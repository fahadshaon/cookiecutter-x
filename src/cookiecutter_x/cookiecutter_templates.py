import json
import logging
import os
from typing import List, Iterator, Dict, Any

import click
from cached_property import cached_property
from cookiecutter.main import cookiecutter

from . import core
from .cli import cli
from .core import TemplateResolver, CCXError
from .template_processor import TemplateProcessor, Variable


@cli.group(
    name="cc",
    help="Manage and process cookiecutter templates"
)
def cookiecutter_cmd():
    pass


@cookiecutter_cmd.command(
    name="list",
    help="List available templates"
)
def list_templates():
    resolver = core.config.cookiecutter_template_resolver()
    for t in resolver.list():
        print(t)


class CookiecutterTemplateProcessor(TemplateProcessor):

    def __init__(self, name: str, resolver: TemplateResolver = None) -> None:

        if resolver is None:
            resolver = core.config.cookiecutter_template_resolver()

        super().__init__(name, resolver)

    @cached_property
    def cookiecutter_data(self) -> Dict[str, Any]:
        cc_path = os.path.join(self.template_path, 'cookiecutter.json')

        if not os.path.exists(cc_path):
            raise CCXError("Invalid template directory, 'cookiecutter.json' file not found.")

        with open(cc_path) as f:
            return json.load(f)

    def get_variables(self) -> Iterator[Variable]:
        for name, default_value in self.cookiecutter_data.items():
            yield Variable(name=name, required=False, default=default_value)

    def process(self, arguments: List[str]):
        extra_context = self.parse_arguments(arguments)

        logging.info(f"Applying template {self.name} in current directory")
        # Allow additional extensions and make default extension optional
        extra_context['_extensions'] = 'cookiecutter_x.extensions.CCXExtension'

        # TODO Handle the overwrite better
        cookiecutter(
            self.template_path,
            no_input=True,
            extra_context=extra_context,
            output_dir=os.path.abspath('.'),
            overwrite_if_exists=self._overwrite
        )

    def cli_command(self) -> str:
        return "cookiecutter-x cc process"


@cookiecutter_cmd.command(
    name="doc",
    help="Print documentation of the template"
)
@click.argument("template")
@click.option('-a', '--all-arguments', help="Print all argument including jinja templates", default=False, is_flag=True)
def print_template_doc(template: str, all_arguments: bool):
    CookiecutterTemplateProcessor(template).print_short_doc(all_arguments)


@cookiecutter_cmd.command(
    help="Process a cookiecutter template",
    context_settings={'ignore_unknown_options': True, 'allow_extra_args': True}
)
@click.argument('template')
@click.option('-w', '--overwrite', is_flag=True, help="Overwrite existing file", default=False)
@click.pass_context
def process(ctx, template: str, overwrite: bool):
    CookiecutterTemplateProcessor(template) \
        .build_parser() \
        .overwrite(overwrite) \
        .process(list(ctx.args))
