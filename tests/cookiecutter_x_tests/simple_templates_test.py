import os
from unittest.mock import patch, PropertyMock

from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x.core import TemplateResolver
from cookiecutter_x.simple_templates import SimpleTemplateProcessor


class SimpleTemplateProcessorTests(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

        self.base = '/ccx-templates/simple-templates'

        script_contents = '''#!/usr/bin/env bash

set -euo pipefail

echo "{{ filename }}"

'''
        config_contents = '''name: bash
description: Create a bash script for managing multiple commands
variables:
  filename:
    required: false
    type: string
    default: run.sh

files:
  - name: bash_script.sh
    output: "{{ filename }}"
    executable: true
'''

        self.fs.create_file(f"{self.base}/bash/bash_script.sh", contents=script_contents)
        self.fs.create_file(f"{self.base}/bash/ccx.yml", contents=config_contents)

        self.resolver = TemplateResolver([self.base])
        self.template_processor = SimpleTemplateProcessor("bash", self.resolver)

        self.expected_output = '''#!/usr/bin/env bash

set -euo pipefail

echo "run.sh"
'''

    def tearDown(self) -> None:
        super().tearDown()

    def test_data(self):
        data = self.template_processor.data
        expected = {
            'name': 'bash',
            'description': 'Create a bash script for managing multiple commands',
            'variables': {
                'filename': {'required': False, 'type': 'string', 'default': 'run.sh'}
            },
            'files': [
                {'name': 'bash_script.sh', 'output': '{{ filename }}', 'executable': True}
            ]
        }

        self.assertDictEqual(expected, data)

    def test_get_variables(self):
        variables = list(self.template_processor.get_variables())
        self.assertEqual(1, len(variables))

        var = variables[0]

        self.assertEqual("filename", var.name)
        self.assertEqual("run.sh", var.default)
        self.assertFalse(var.required)

    def test_process(self):
        self.template_processor.process(['--filename', 'run.sh'])
        self.assertTrue(os.path.exists('run.sh'))

        with open('run.sh') as f:
            self.assertEqual(self.expected_output, f.read())

    def test_process_no_overwrite(self):
        self.fs.create_file('run.sh', contents='#!/usr/bin/env bash')

        with self.assertRaises(Exception) as context:
            self.template_processor.process(['--filename', 'run.sh'])

        self.assertEqual("Destination file ./run.sh exists; to overwrite pass overwrite flag", str(context.exception))

    def test_process_overwrite(self):
        self.fs.create_file('run.sh', contents='#!/usr/bin/env bash')

        self.template_processor.overwrite(True).process(['--filename', 'run.sh'])

        with open('run.sh') as f:
            self.assertEqual(self.expected_output, f.read())


class SimpleTemplateProcessorWithoutVariables(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

    def test_no_variable(self):
        self.base = '/templates'
        self.fs.create_dir(f"{self.base}/bash/bash_script.sh")

        self.resolver = TemplateResolver([self.base])
        with patch(
                'cookiecutter_x.simple_templates.SimpleTemplateProcessor.data',
                new_callable=PropertyMock, return_value={'name': 'bash'}
        ):
            processor = SimpleTemplateProcessor('bash', self.resolver)
            self.assertDictEqual({'name': 'bash'}, processor.data)

            with self.assertRaises(Exception) as context:
                # Since this is a generator need to invoke the generation
                list(processor.get_variables())

        self.assertEqual("Template without variables; just copy the files.", str(context.exception))
