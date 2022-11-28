import logging

import coloredlogs

from .cli import cli
# Here we are loading the modules that have commands.
# Do NOT remove these
from . import simple_templates
from . import cookiecutter_templates
from . import quick_start


def main():
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    coloredlogs.install(level=logging.INFO, logger=logging.getLogger(), fmt=logging_format)

    cli()


if __name__ == '__main__':
    main()
