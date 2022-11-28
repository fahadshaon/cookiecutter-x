import logging
import os
from typing import Any, Dict, List, Iterator

import click
from cached_property import cached_property
from jinja2 import Environment

from . import core
from . import utils
from .cli import cli
from .core import TemplateResolver
from .template_processor import TemplateProcessor, Variable


class SimpleTemplateProcessor(TemplateProcessor):

    def __init__(self, name: str, resolver: TemplateResolver = None) -> None:
        if resolver is None:
            resolver = core.config.simple_template_resolver()

        super().__init__(name, resolver)

    def get_variables(self) -> Iterator[Variable]:
        if 'variables' not in self.data:
            raise core.CCXError("Template without variables; just copy the files.")

        for name, attrs in self.data['variables'].items():
            required = 'required' in attrs and attrs['required']
            default = attrs['default'] if 'default' in attrs else None
            var_type = attrs['type'] if 'type' in attrs else None

            yield Variable(name=name, required=required, default=default, var_type=var_type)

    def cli_command(self) -> str:
        return "cookiecutter-x simple process"

    def process(self, arguments: List[str]) -> None:
        self.process_files(self.parse_arguments(arguments))

    def process_files(self, variables: Dict[str, Any]):
        for f in self.data['files']:
            self.process_single_file(variables, f)

    @cached_property
    def template_env(self) -> Environment:
        from .extensions import CCXExtension

        env = Environment(lstrip_blocks=True, trim_blocks=True)
        env.add_extension(CCXExtension)

        return env

    def process_single_file(self, variables: Dict[str, Any], file_info: Dict[str, str]):
        out_filename_template = self.template_env.from_string(file_info['output'])
        out_filename = out_filename_template.render(**variables)

        out_file_path = out_filename if os.path.isabs(out_filename) \
            else os.path.join('.', out_filename)

        in_file = os.path.join(self.template_path, file_info['name'])
        self._process_single_template(in_file, out_file_path, variables)

        if 'executable' in file_info and file_info['executable']:
            utils.make_file_executable(out_file_path)

    def _process_single_template(self, template_file: str, output_file: str, variables: Dict[str, Any]):
        if os.path.exists(output_file) and not self._overwrite:
            raise core.CCXError(f"Destination file {output_file} exists; to overwrite pass overwrite flag")

        with open(template_file) as f:
            template_content = f.read()

        content = self.template_env.from_string(template_content).render(**variables)

        with open(output_file, 'w') as f:
            logging.info(f"Writing {output_file}")
            f.write(content)


@cli.group(
    name="simple",
    help="Simple script or generation"
)
def simple():
    pass


@simple.command(
    name="list",
    help="List name of all simple templates"
)
def list_templates():
    resolver = core.config.simple_template_resolver()
    for t in resolver.list():
        print(t)


@simple.command(
    name='doc',
    help="Print template help, showing available variables and command"
)
@click.argument('template')
@click.option('-a', '--all-arguments', help="Print all argument including jinja templates", default=False, is_flag=True)
def print_template_doc(template: str, all_arguments: bool):
    SimpleTemplateProcessor(template).print_short_doc(all_arguments)


@simple.command(
    name="process",
    help="Apply a simple template",
    context_settings={'ignore_unknown_options': True, 'allow_extra_args': True}
)
@click.argument('template')
@click.option('-w', '--overwrite', is_flag=True, help="Overwrite existing file", default=False)
@click.pass_context
def process(ctx, template: str, overwrite: bool):
    SimpleTemplateProcessor(template) \
        .build_parser() \
        .overwrite(overwrite) \
        .process(list(ctx.args))
