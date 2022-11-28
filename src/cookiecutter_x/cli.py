import click

cli = click.Group(
    name='cookiecutter-x', help="Cookiecutter eXtended",
    context_settings={'help_option_names': ['-h', '--help']}
)
