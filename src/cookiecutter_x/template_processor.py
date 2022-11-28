import argparse
import os
from abc import ABC, abstractmethod
from shlex import quote
from typing import Any, Dict, List, Iterator

import yaml
from cached_property import cached_property

from . import utils
from .core import TemplateResolver, CCXError


class Variable:

    def __init__(self, name: str, required: bool, default: Any = None, var_type: str = None) -> None:
        # Optional variables must have type defined.
        super().__init__()
        self.name = name
        self.required = required
        self.default = default
        self.var_type = var_type if var_type else self.get_type_from_value(default)

        # Corner case - variable is required but no default or the type is provided
        if required and (not default and not self.var_type):
            self.var_type = 'string'

        if self.var_type not in ['string', 'boolean', 'number', 'list', 'dictionary']:
            raise CCXError(f"Unable to determine the variable type for {name}")

    @staticmethod
    def get_type_from_value(value: Any) -> str:
        if isinstance(value, bool):
            return 'boolean'

        if isinstance(value, str):
            return 'string'

        if isinstance(value, int) or isinstance(value, float):
            return 'number'

        if isinstance(value, list):
            return 'list'

        if isinstance(value, dict):
            return 'dictionary'


class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise ArgumentParserError(message)


class TemplateProcessor(ABC):
    def __init__(self, name: str, resolver: TemplateResolver) -> None:
        super().__init__()

        self.name = name
        self.template_path = resolver.get_path(name)

        self._parser = None
        self._overwrite = False

    def overwrite(self, overwrite: bool) -> "TemplateProcessor":
        self._overwrite = overwrite
        return self

    @abstractmethod
    def get_variables(self) -> Iterator[Variable]:
        pass

    @cached_property
    def variables(self) -> List[Variable]:
        return list(self.get_variables())

    def build_parser(self) -> "TemplateProcessor":
        self._parser = ThrowingArgumentParser(description='Process template variables')

        # Consider adding short option; will need to find unique char per command,
        # final command might become unintuitive
        for variable in self.get_variables():
            argument_properties = {
                'required': variable.required
            }

            if variable.default:
                argument_properties['default'] = variable.default

            if variable.var_type == 'boolean':

                self._parser.add_argument(
                    f"--{variable.name}", default=variable.default or False,
                    type=lambda x: str(x).lower() in ['true', 't', 'yes', 'y', 1]
                )
            else:
                self._parser.add_argument(f"--{variable.name}", **argument_properties)

        return self

    def parse_arguments(self, arguments: List[str]) -> Dict[str, Any]:
        if not self._parser:
            self.build_parser()

        args = self._parser.parse_args(arguments)
        return vars(args)

    def print_short_doc(self, all_arguments: bool):
        self.template_doc_printer().print_short_doc(all_arguments)

    @cached_property
    def data(self) -> Dict[str, Any]:
        y = os.path.join(self.template_path, 'ccx.yml')
        if not os.path.exists(y):
            return {}

        with open(y) as f:
            return yaml.safe_load(f)

    @abstractmethod
    def cli_command(self) -> str:
        pass

    def template_doc_printer(self) -> "TemplateDocPrinter":
        return TemplateDocPrinter(
            name=self.name,
            description=self.data['description'] if 'description' in self.data else '',
            post_gen=self.data['post_gen'] if 'post_gen' in self.data else '',
            variables=self.variables,
            cli_command=self.cli_command()
        )


class TemplateDocPrinter:
    def __init__(
            self, name: str, cli_command: str, description: str = None,
            variables: List[Variable] = None, post_gen: str = None
    ) -> None:
        super().__init__()

        self.name = name
        self.cli_command = cli_command

        self.description = description
        self.variables = variables if variables else []
        self.post_gen = post_gen

    def print_short_doc(self, all_arguments: bool):
        sections = [
            (self.name, self.description),
            ('Variables', list(self.variables_to_str_list())),
            ('Run', self.generate_command(all_arguments))
        ]

        if self.post_gen:
            sections.append(("Post generation action", self.post_gen))

        print(utils.format_sections(sections))

    def variables_to_str_list(self) -> Iterator[str]:
        for v in self.variables:
            if v.name.startswith('_'):
                # Cookiecutter internal variables can't be modified from command line
                continue

            if v.required:
                yield f"{v.name} (required)"
            else:
                yield f"{v.name} (default: {v.default})"

    def generate_command(self, print_all_arguments: bool = False):
        return f"    {self.cli_command} {self.name} {self.generate_args(self.variables, print_all_arguments)}"

    @staticmethod
    def generate_args(variables: List[Variable], print_all_arguments: bool = False) -> str:
        args = []

        for v in variables:

            if v.var_type == "list" or v.var_type == "dictionary":
                # Will implemented once needed
                continue

            if v.required:
                args.append(f"--{v.name}")
                if v.default is None:
                    args.append("<value>")
                else:
                    args.append(v.default)

                continue

            # Non-required attributes
            if v.var_type == "string":

                if v.default is None:
                    arg = "<value>"
                elif '{{' in v.default:

                    # Very special case for jinja templates
                    if print_all_arguments:
                        arg = v.default
                    else:
                        # This branch is tested but in coverage==6.2,
                        # it is marked as not covered!
                        continue
                else:
                    arg = v.default

            elif v.var_type == "boolean":
                if v.default is None:
                    arg = "<true/false>"
                else:
                    arg = str(v.default).lower()

            else:
                raise CCXError(f"Unsupported variable type {v.var_type} in command generation")

            args.append(f"--{v.name}")
            args.append(arg)

        return ' '.join(quote(str(q)) for q in args)
