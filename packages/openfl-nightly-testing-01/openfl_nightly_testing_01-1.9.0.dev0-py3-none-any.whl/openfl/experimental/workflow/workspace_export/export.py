# Copyright 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


"""Workspace Export module."""

import ast
import importlib
import inspect
import re
import shutil
import sys
from logging import getLogger
from pathlib import Path
from shutil import copytree
from typing import Any, Dict, Optional, Tuple

import nbformat
import yaml
from nbdev.export import nb_export

from openfl.experimental.workflow.federated.plan import Plan
from openfl.experimental.workflow.interface.cli.cli_helper import print_tree

logger = getLogger(__name__)


class WorkspaceExport:
    """Convert a LocalRuntime Jupyter Notebook to Aggregator based
    FederatedRuntime Workflow.

    Attributes:
        notebook_path: Absolute path of jupyter notebook.
        template_workspace_path: Path to template workspace provided with
            OpenFL.
        output_workspace_path: Output directory for new generated workspace
            (default="/tmp").
    """

    def __init__(self, notebook_path: str, output_workspace: str) -> None:
        """Initialize a WorkspaceExport object.

        Args:
            notebook_path (str): Path to Jupyter notebook.
            output_workspace (str): Path to output_workspace to be
                generated.
        """

        self.notebook_path = Path(notebook_path).resolve()
        # Check if the Jupyter notebook exists
        if not self.notebook_path.exists() or not self.notebook_path.is_file():
            raise FileNotFoundError(f"The Jupyter notebook at {notebook_path} does not exist.")

        self.output_workspace_path = Path(output_workspace).resolve()
        # Regenerate the workspace if it already exists
        if self.output_workspace_path.exists():
            shutil.rmtree(self.output_workspace_path)
        self.output_workspace_path.parent.mkdir(parents=True, exist_ok=True)

        self.template_workspace_path = (
            Path(f"{__file__}")
            .parent.parent.parent.parent.parent.joinpath(
                "openfl-workspace",
                "experimental",
                "workflow",
                "AggregatorBasedWorkflow",
                "template_workspace",
            )
            .resolve(strict=True)
        )

        # Copy template workspace to output directory
        self.created_workspace_path = Path(
            copytree(self.template_workspace_path, self.output_workspace_path)
        )
        logger.info(f"Copied template workspace to {self.created_workspace_path}")

        logger.info("Converting jupter notebook to python script...")
        export_filename = self.__get_exp_name()
        if export_filename is None:
            raise NameError(
                "Please include `#| default_exp <experiment_name>` in "
                "the first cell of the notebook."
            )
        self.script_path = Path(
            self.__convert_to_python(
                self.notebook_path,
                self.created_workspace_path.joinpath("src"),
                f"{export_filename}.py",
            )
        ).resolve()

        # Generated python script name without .py extension
        self.script_name = self.script_path.name.split(".")[0].strip()
        # Comment flow.run() so when script is imported flow does not start
        # executing
        self.__comment_flow_execution()
        # This is required as Ray created actors too many actors when
        # backend="ray" # NOQA
        self.__change_runtime()

    def __get_exp_name(self) -> None:
        """Fetch the experiment name from the Jupyter notebook."""
        with open(str(self.notebook_path), "r") as f:
            notebook_content = nbformat.read(f, as_version=nbformat.NO_CONVERT)

        for cell in notebook_content.cells:
            if cell.cell_type == "code":
                code = cell.source
                match = re.search(r"#\s*\|\s*default_exp\s+(\w+)", code)
                if match:
                    logger.info(f"Retrieved {match.group(1)} from default_exp")
                    return match.group(1)
        return None

    def __convert_to_python(self, notebook_path: Path, output_path: Path, export_filename) -> Path:
        """Converts a Jupyter notebook to a Python script.

        Args:
            notebook_path (Path): The path to the Jupyter notebook file
                to be converted.
            output_path (Path): The directory where the exported Python
                script should be saved.
            export_filename: The name of the exported Python script file.
        """
        nb_export(notebook_path, output_path)

        return Path(output_path).joinpath(export_filename).resolve()

    def __comment_flow_execution(self) -> None:
        """In the python script search for ".run()" and comment it."""
        with open(self.script_path, "r") as f:
            data = f.readlines()
        for idx, line in enumerate(data):
            if ".run()" in line:
                data[idx] = f"# {line}"
        with open(self.script_path, "w") as f:
            f.writelines(data)

    def __change_runtime(self) -> None:
        """Change the LocalRuntime backend from ray to single_process."""
        with open(self.script_path, "r") as f:
            data = f.read()

        if "backend='ray'" in data or 'backend="ray"' in data:
            data = data.replace("backend='ray'", "backend='single_process'").replace(
                'backend="ray"', 'backend="single_process"'
            )

        with open(self.script_path, "w") as f:
            f.write(data)

    def __get_class_arguments(self, class_name) -> list:
        """Given the class name returns expected class arguments.

        Args:
            class_name (str): Name of the class
        """
        # Import python script if not already
        if not hasattr(self, "exported_script_module"):
            self.__import_exported_script()

        # Find class from imported python script module
        for idx, attr in enumerate(self.available_modules_in_exported_script):
            if attr == class_name:
                cls = getattr(
                    self.exported_script_module,
                    self.available_modules_in_exported_script[idx],
                )

        # If class not found
        if "cls" not in locals():
            raise NameError(f"{class_name} not found.")

        if inspect.isclass(cls):
            # Check if the class has an __init__ method
            if "__init__" in cls.__dict__:
                init_signature = inspect.signature(cls.__init__)
                # Extract the parameter names (excluding 'self', 'args', and
                # 'kwargs')
                arg_names = [
                    param
                    for param in init_signature.parameters
                    if param not in ("self", "args", "kwargs")
                ]
                return arg_names
            return []
        logger.error(f"{cls} is not a class")

    def __get_class_name_and_sourcecode_from_parent_class(
        self, parent_class
    ) -> Optional[Tuple[Optional[str], Optional[str]]]:
        """Provided the parent_class name returns derived class source code and
        name.

        Args:
            parent_class: FLSpec instance
        """
        # Import python script if not already
        if not hasattr(self, "exported_script_module"):
            self.__import_exported_script()

        # Going though all attributes in imported python script
        for attr in self.available_modules_in_exported_script:
            t = getattr(self.exported_script_module, attr)
            if inspect.isclass(t) and t != parent_class and issubclass(t, parent_class):
                return inspect.getsource(t), attr

        return None, None

    def __extract_class_initializing_args(self, class_name) -> Dict[str, Any]:
        """Provided name of the class returns expected arguments and its
        values in the form of a dictionary.

        Args:
            class_name (str): Name of the class
        """
        instantiation_args = {"args": {}, "kwargs": {}}

        with open(self.script_path, "r") as s:
            tree = ast.parse(s.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == class_name:
                        # We found an instantiation of the class
                        instantiation_args["args"] = self._extract_positional_args(node.args)
                        instantiation_args["kwargs"] = self._extract_keyword_args(node.keywords)

        return instantiation_args

    def _extract_positional_args(self, args) -> Dict[str, Any]:
        """Extract positional arguments from the AST nodes."""
        positional_args = {}
        for arg in args:
            if isinstance(arg, ast.Name):
                positional_args[arg.id] = arg.id
            elif isinstance(arg, ast.Constant):
                positional_args[arg.s] = ast.unparse(arg)
            else:
                positional_args[arg.arg] = ast.unparse(arg).strip()
        return positional_args

    def _extract_keyword_args(self, keywords) -> Dict[str, Any]:
        """Extract keyword arguments from the AST nodes."""
        keyword_args = {}
        for kwarg in keywords:
            value = ast.unparse(kwarg.value).strip()
            value = self._clean_value(value)
            try:
                value = ast.literal_eval(value)
            except ValueError:
                pass
            keyword_args[kwarg.arg] = value
        return keyword_args

    def _clean_value(self, value: str) -> str:
        """Clean the value by removing unnecessary parentheses or brackets."""
        if value.startswith("(") and "," not in value:
            value = value.lstrip("(").rstrip(")")
        if value.startswith("[") and "," not in value:
            value = value.lstrip("[").rstrip("]")
        return value

    def __import_exported_script(self) -> None:
        """
        Imports generated python script with help of importlib
        """

        sys.path.append(str(self.script_path.parent))
        self.exported_script_module = importlib.import_module(self.script_name)
        self.available_modules_in_exported_script = dir(self.exported_script_module)

    def __read_yaml(self, path) -> None:
        with open(path, "r") as y:
            return yaml.safe_load(y)

    def __write_yaml(self, path, data) -> None:
        with open(path, "w") as y:
            yaml.safe_dump(data, y)

    @classmethod
    def export_federated(
        cls, notebook_path: str, output_workspace: str, director_fqdn: str, tls: bool = False
    ) -> Tuple[str, str]:
        """Exports workspace for FederatedRuntime.

        Args:
            notebook_path (str): Path to the Jupyter notebook.
            output_workspace (str): Path for the generated workspace directory.
            director_fqdn (str): Fully qualified domain name of the director node.
            tls (bool, optional): Whether to use TLS for the connection.

        Returns:
            Tuple[str, str]: A tuple containing:
                (archive_path, flow_class_name).
        """
        instance = cls(notebook_path, output_workspace)
        instance.generate_requirements()
        instance.generate_plan_yaml(director_fqdn, tls)
        instance._clean_generated_workspace()
        print_tree(output_workspace, level=2)
        return instance.generate_experiment_archive()

    @classmethod
    def export(cls, notebook_path: str, output_workspace: str) -> None:
        """Exports workspace to output_workspace.

        Args:
            notebook_path (str): Path to the Jupyter notebook.
            output_workspace (str): Path for the generated workspace directory.
        """
        instance = cls(notebook_path, output_workspace)
        instance.generate_requirements()
        instance.generate_plan_yaml()
        instance.generate_data_yaml()
        print_tree(output_workspace, level=2)

    def generate_experiment_archive(self) -> Tuple[str, str]:
        """
        Create archive of the generated workspace

        Returns:
            Tuple[str, str]: A tuple containing:
                (generated_workspace_path, archive_path, flow_class_name).
        """
        parent_directory = self.output_workspace_path.parent
        archive_path = parent_directory / "experiment"

        # Create a ZIP archive of the generated_workspace directory
        arch_path = shutil.make_archive(str(archive_path), "zip", str(self.output_workspace_path))

        print(f"Archive created at {archive_path}.zip")

        return arch_path, self.flow_class_name

    # Have to do generate_requirements before anything else
    # because these !pip commands needs to be removed from python script
    def generate_requirements(self) -> None:
        """Finds pip libraries mentioned in exported python script and append
        in workspace/requirements.txt."""
        data = None
        with open(self.script_path, "r") as f:
            requirements = []
            line_nos = []
            data = f.readlines()
            for i, line in enumerate(data):
                line = line.strip()
                if "pip install" in line:
                    line_nos.append(i)
                    # Avoid commented lines, libraries from *.txt file, or openfl.git
                    # installation
                    if not line.startswith("#") and "-r" not in line and "openfl.git" not in line:
                        requirements.append(f"{line.split(' ')[-1].strip()}\n")

        requirements_filepath = str(
            self.created_workspace_path.joinpath("requirements.txt").resolve()
        )

        # Write libraries found in requirements.txt
        with open(requirements_filepath, "a") as f:
            f.writelines(requirements)

        # Delete pip requirements from python script
        # if not we won't be able to import python script.
        with open(self.script_path, "w") as f:
            for i, line in enumerate(data):
                if i not in line_nos:
                    f.write(line)

    def _clean_generated_workspace(self) -> None:
        """
        Remove cols.yaml and data.yaml from the generated workspace
        as these are not needed in FederatedRuntime (Director based workflow)

        """
        cols_file = self.output_workspace_path.joinpath("plan", "cols.yaml")
        data_file = self.output_workspace_path.joinpath("plan", "data.yaml")

        if cols_file.exists():
            cols_file.unlink()
        if data_file.exists():
            data_file.unlink()

    def generate_plan_yaml(self, director_fqdn: str = None, tls: bool = False) -> None:
        """
        Generates plan.yaml

        Args:
            director_fqdn (str): Fully qualified domain name of the director node.
            tls (bool, optional): Whether to use TLS for the connection.
        """
        flspec = importlib.import_module("openfl.experimental.workflow.interface").FLSpec
        # Get flow classname
        _, self.flow_class_name = self.__get_class_name_and_sourcecode_from_parent_class(flspec)
        # Get expected arguments of flow class
        self.flow_class_expected_arguments = self.__get_class_arguments(self.flow_class_name)
        # Get provided arguments to flow class
        self.arguments_passed_to_initialize = self.__extract_class_initializing_args(
            self.flow_class_name
        )

        plan = self.created_workspace_path.joinpath("plan", "plan.yaml").resolve()
        data = self.__read_yaml(plan)
        if data is None:
            data = {}
            data["federated_flow"] = {"settings": {}, "template": ""}

        data["federated_flow"]["template"] = f"src.{self.script_name}.{self.flow_class_name}"

        def update_dictionary(args: dict, data: dict, dtype: str = "args"):
            for idx, (k, v) in enumerate(args.items()):
                if dtype == "args":
                    v = getattr(self.exported_script_module, str(k), None)
                    if v is not None and type(v) not in (int, str, bool):
                        v = f"src.{self.script_name}.{k}"
                    k = self.flow_class_expected_arguments[idx]
                elif dtype == "kwargs":
                    if v is not None and type(v) not in (int, str, bool):
                        v = f"src.{self.script_name}.{k}"
                data["federated_flow"]["settings"].update({k: v})

        # Find positional arguments of flow class and it's values
        pos_args = self.arguments_passed_to_initialize["args"]
        update_dictionary(pos_args, data, dtype="args")
        # Find kwargs of flow class and it's values
        kw_args = self.arguments_passed_to_initialize["kwargs"]
        update_dictionary(kw_args, data, dtype="kwargs")

        # Updating the aggregator address with director's hostname and tls settings in plan.yaml
        if director_fqdn:
            network_settings = Plan.parse(plan).config["network"]
            data["network"] = network_settings
            data["network"]["settings"]["agg_addr"] = director_fqdn
            data["network"]["settings"]["tls"] = tls

        self.__write_yaml(plan, data)

    def generate_data_yaml(self) -> None:
        """Generates data.yaml."""
        # Import python script if not already
        if not hasattr(self, "exported_script_module"):
            self.__import_exported_script()

        self._find_flow_class_name_if_needed()
        # Import flow class
        federated_flow_class = getattr(self.exported_script_module, self.flow_class_name)

        flow_name, runtime = self._find_runtime_instance(federated_flow_class)
        data_yaml = self.created_workspace_path.joinpath("plan", "data.yaml").resolve()
        data = self._read_or_initialize_yaml(data_yaml)
        runtime_name = "runtime_local"
        runtime_created = self._process_aggregator(runtime, data, flow_name, runtime_name)
        self._process_collaborators(runtime, data, flow_name, runtime_created, runtime_name)
        self.__write_yaml(data_yaml, data)

    def _find_flow_class_name_if_needed(self):
        """Find the flow class name if not already found."""
        if not hasattr(self, "flow_class_name"):
            flspec = importlib.import_module("openfl.experimental.workflow.interface").FLSpec
            _, self.flow_class_name = self.__get_class_name_and_sourcecode_from_parent_class(flspec)

    def _find_runtime_instance(self, federated_flow_class):
        """Find the runtime instance."""
        for t in self.available_modules_in_exported_script:
            t = getattr(self.exported_script_module, t)
            if isinstance(t, federated_flow_class):
                if not hasattr(t, "_runtime"):
                    raise AttributeError("Unable to locate LocalRuntime instantiation")
                runtime = t._runtime
                if not hasattr(runtime, "collaborators"):
                    raise AttributeError("LocalRuntime instance does not have collaborators")
                return runtime
        raise AttributeError("Runtime instance not found")

    def _read_or_initialize_yaml(self, data_yaml):
        """Read or initialize the YAML data."""
        data = self.__read_yaml(data_yaml)
        return data if data is not None else {}

    def _process_aggregator(self, runtime, data, flow_name, runtime_name):
        """Process the aggregator details."""
        aggregator = runtime._aggregator
        runtime_created = False
        private_attrs_callable = aggregator.private_attributes_callable
        aggregator_private_attributes = aggregator.private_attributes

        if private_attrs_callable is not None:
            data["aggregator"] = {
                "callable_func": {
                    "settings": {},
                    "template": f"src.{self.script_name}.{private_attrs_callable.__name__}",
                }
            }
            arguments_passed_to_initialize = self.__extract_class_initializing_args("Aggregator")[
                "kwargs"
            ]
            agg_kwargs = aggregator.kwargs
            for key, value in agg_kwargs.items():
                if isinstance(value, (int, str, bool)):
                    data["aggregator"]["callable_func"]["settings"][key] = value
                else:
                    arg = arguments_passed_to_initialize[key]
                    value = f"src.{self.script_name}.{arg}"
                    data["aggregator"]["callable_func"]["settings"][key] = value
        elif aggregator_private_attributes:
            runtime_created = True
            with open(self.script_path, "a") as f:
                f.write(f"\n{runtime_name} = {flow_name}._runtime\n")
                f.write(
                    f"\naggregator_private_attributes = "
                    f"{runtime_name}._aggregator.private_attributes\n"
                )
            data["aggregator"] = {
                "private_attributes": f"src.{self.script_name}.aggregator_private_attributes"
            }
        return runtime_created

    def _process_collaborators(self, runtime, data, flow_name, runtime_created, runtime_name):
        """Process the collaborators."""
        collaborators = runtime._LocalRuntime__collaborators
        arguments_passed_to_initialize = self.__extract_class_initializing_args("Collaborator")[
            "kwargs"
        ]
        runtime_collab_created = False
        for collab in collaborators.values():
            collab_name = collab.get_name()
            callable_func = collab.private_attributes_callable
            private_attributes = collab.private_attributes

            if callable_func:
                if collab_name not in data:
                    data[collab_name] = {"callable_func": {"settings": {}, "template": None}}
                kw_args = runtime.get_collaborator_kwargs(collab_name)
                for key, value in kw_args.items():
                    if key == "private_attributes_callable":
                        value = f"src.{self.script_name}.{value}"
                        data[collab_name]["callable_func"]["template"] = value
                    elif isinstance(value, (int, str, bool)):
                        data[collab_name]["callable_func"]["settings"][key] = value
                    else:
                        arg = arguments_passed_to_initialize[key]
                        value = f"src.{self.script_name}.{arg}"
                        data[collab_name]["callable_func"]["settings"][key] = value
            elif private_attributes:
                with open(self.script_path, "a") as f:
                    if not runtime_created:
                        f.write(f"\n{runtime_name} = {flow_name}._runtime\n")
                        runtime_created = True
                    if not runtime_collab_created:
                        f.write(
                            f"\nruntime_collaborators = {runtime_name}._LocalRuntime__collaborators"
                        )
                        runtime_collab_created = True
                    f.write(
                        f"\n{collab_name}_private_attributes = "
                        f"runtime_collaborators['{collab_name}'].private_attributes"
                    )
                data[collab_name] = {
                    "private_attributes": f"src.{self.script_name}.{collab_name}_private_attributes"
                }
