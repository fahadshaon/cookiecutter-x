import json
import os
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x.cookiecutter_templates import CookiecutterTemplateProcessor
from cookiecutter_x.core import TemplateResolver


class CookiecutterTemplateProcessorTests(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()
        setup_content = '''import setuptools

setuptools.setup(
    name="{{cookiecutter.app_name}}",
    version="0.0.2"
)
'''
        self.base = '/packages'
        self.context = {
            'app_name': 'cookiecutter-x-test'
        }

        self.fs.create_file(f"{self.base}/python/{{{{cookiecutter.app_name}}}}/setup.py", contents=setup_content)
        self.fs.create_file(f"{self.base}/python/cookiecutter.json", contents=json.dumps(self.context, indent=4))

        self.resolver = TemplateResolver([self.base])
        self.template_processor = CookiecutterTemplateProcessor("python", self.resolver)

    def tearDown(self) -> None:
        super().tearDown()

    def test_cookiecutter_data(self):
        self.assertDictEqual(self.context, self.template_processor.cookiecutter_data)

    def test_get_variables(self):
        variables = list(self.template_processor.get_variables())
        self.assertEqual(1, len(variables))

        var = variables[0]

        self.assertEqual("app_name", var.name)
        self.assertEqual("cookiecutter-x-test", var.default)
        self.assertEqual(False, var.required)
        self.assertEqual("string", var.var_type)

    def test_process(self):
        with patch('cookiecutter_x.cookiecutter_templates.cookiecutter', return_value='') as mock:
            # Patching 'cookiecutter.main.cookiecutter' does not seem to work

            self.template_processor.process(['--app_name', 'test-project'])

            mock.assert_called_once_with(
                '/packages/python',
                no_input=True,
                extra_context={
                    'app_name': 'test-project',
                    '_extensions': 'cookiecutter_x.extensions.CCXExtension'
                },
                output_dir=os.path.abspath('.'),
                overwrite_if_exists=False
            )

    def test_invalid_template_dir(self):
        with self.assertRaises(Exception) as context:
            self.fs.remove(f"{self.base}/python/cookiecutter.json")
            template_processor = CookiecutterTemplateProcessor("python", self.resolver)
            data = template_processor.cookiecutter_data

        self.assertEqual("Invalid template directory, 'cookiecutter.json' file not found.", str(context.exception))
