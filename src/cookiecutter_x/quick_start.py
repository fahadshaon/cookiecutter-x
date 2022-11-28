import logging
import os
from typing import Dict

from . import utils
from .cli import cli
from .core import config


@cli.group(
    name="quick-start",
    help="Generate sample configuration and template"
)
def quick_start():
    pass


def sample_config() -> str:
    return '''simple_templates:
  paths:
    - ~/.cookiecutter-x/simple-templates

cookiecutter_templates:
  paths:
    - ~/.cookiecutter-x/cookiecutter-templates
'''


@quick_start.command(
    name="config",
    help="Generate initial configuration if the config does not exist"
)
def generate_config():
    if os.path.exists(config.configs_path):
        logging.warning("Config file exists, not overwriting")
        return

    utils.make_dirs(config.base_path)
    utils.write_content(config.configs_path, sample_config())


def ccp_template_content() -> Dict[str, str]:
    ccx_content = '''name: cpp
description: Generate CPP and H with include protection

variables:
  class_name:
    required: true
    type: string

files:
  - name: cpp.cpp
    output: "{{ class_name | remove_extension }}.cpp"
  - name: cpp.h
    output: "{{ class_name | remove_extension }}.h"
'''

    cpp_content = '''#include "{{ class_name | remove_extension }}.h"
'''

    h_content = '''#ifndef __{{ class_name | remove_extension | snake_case | upper }}_H__
#define __{{ class_name | remove_extension | snake_case | upper }}_H__

class {{class_name}} {

public:
    virtual void action();
};

#endif
'''

    return {
        'ccx': ccx_content,
        'cpp': cpp_content,
        'h': h_content
    }


@quick_start.command(
    name="sample-template",
    help="Generate the cpp sample template from documentation"
)
def generate_sample_template():
    sample_path = config.simple_template_paths[0]
    cpp_template = os.path.join(sample_path, 'cpp')

    if os.path.exists(cpp_template) and len(os.listdir(cpp_template)) > 0:
        logging.warning("CPP sample template exists; not overwriting")
        return

    utils.make_dirs(cpp_template)
    contents = ccp_template_content()

    utils.write_content(os.path.join(cpp_template, 'ccx.yml'), contents['ccx'])
    utils.write_content(os.path.join(cpp_template, 'cpp.cpp'), contents['cpp'])
    utils.write_content(os.path.join(cpp_template, 'cpp.h'), contents['h'])
