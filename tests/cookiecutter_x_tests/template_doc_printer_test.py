import contextlib
import io
from unittest.case import TestCase

from cookiecutter_x.template_processor import TemplateDocPrinter, Variable


class VariableTest(TestCase):
    def test_invalid_type(self):
        with self.assertRaises(Exception) as context:
            Variable("app_name", False)

        self.assertEqual("Unable to determine the variable type for app_name", str(context.exception))


class TemplateDocPrinterTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.name = 'python-package'
        self.variables = [
            Variable("app_name", True),
            Variable("app_description", required=False, default="Awesomeness"),
            Variable("logs", required=False, default=True),
            Variable("extra_logs", required=False, default=False),
        ]

        self.description = 'Template description'
        self.post_gen = 'Some post generation message'

        self.command = 'cookiecutter-x cc process'
        self.doc_printer = TemplateDocPrinter(self.name, self.command, self.description, self.variables, self.post_gen)

    def test_print_short_doc(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.doc_printer.print_short_doc(False)

        expected = '''
python-package
--------------
Template description

Variables
---------
- app_name (required)
- app_description (default: Awesomeness)
- logs (default: True)
- extra_logs (default: False)

Run
---
    cookiecutter-x cc process python-package --app_name '<value>' --app_description Awesomeness --logs true --extra_logs false

Post generation action
----------------------
Some post generation message

'''

        self.assertEqual(expected, f.getvalue())

    def test_variable_to_args(self):
        args_str = TemplateDocPrinter.generate_args([Variable("app_name", True)], False)
        self.assertEqual("--app_name '<value>'", args_str)

        args_str = TemplateDocPrinter.generate_args([Variable("app_name", True, "awesomeness")], False)
        self.assertEqual("--app_name awesomeness", args_str)

        args_str = TemplateDocPrinter.generate_args([Variable("app_name", False, "awesomeness")], False)
        self.assertEqual("--app_name awesomeness", args_str)

    def test_variables_to_args(self):
        variables = [
            Variable("app_name", True),
            Variable("app_description", False, "Awesomeness")
        ]

        args_str = TemplateDocPrinter.generate_args(variables, False)
        self.assertEqual("--app_name '<value>' --app_description Awesomeness", args_str)

    def test_optional_variables_to_args(self):
        variables = [
            Variable("app_name", True),
            Variable("app_description", False, var_type="string")
        ]

        args_str = TemplateDocPrinter.generate_args(variables, False)
        self.assertEqual("--app_name '<value>' --app_description '<value>'", args_str)

    def test_optional_boolean_variables_to_args(self):
        variables = [
            Variable("app_name", True),
            Variable("log", False, var_type="boolean")
        ]

        args_str = TemplateDocPrinter.generate_args(variables, False)
        self.assertEqual("--app_name '<value>' --log '<true/false>'", args_str)

    def test_jinja_variables_to_args(self):
        variables = [
            Variable("app_name", True),
            Variable("app_description", False, default="{{ cookicutter.app_name | to_lower }}")
        ]

        # When not required command generator does not print the jinja templates
        args_str = TemplateDocPrinter.generate_args(variables, False)
        self.assertEqual("--app_name '<value>'", args_str)

        args_str = TemplateDocPrinter.generate_args(variables, True)
        self.assertEqual("--app_name '<value>' --app_description '{{ cookicutter.app_name | to_lower }}'", args_str)

        variables = [
            Variable("app_name", True),
            Variable("app_description", False, default="{{ cookicutter.app_name | to_lower }}")
        ]
        args_str = TemplateDocPrinter.generate_args(variables, False)
        self.assertEqual("--app_name '<value>'", args_str)
