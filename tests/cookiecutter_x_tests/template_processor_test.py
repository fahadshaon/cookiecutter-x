from typing import Iterator

from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x.core import TemplateResolver
from cookiecutter_x.template_processor import TemplateProcessor, Variable, TemplateDocPrinter


class DummyTemplateProcessor(TemplateProcessor):

    def cli_command(self) -> str:
        return "cookiecutter-x dummy"

    def __init__(self, name: str, resolver: TemplateResolver) -> None:
        super().__init__(name, resolver)

    def get_variables(self) -> Iterator[Variable]:
        yield Variable("app_name", True)
        yield Variable("app_description", required=False, default="Awesomeness")
        yield Variable("logs", required=False, default=True)
        yield Variable("extra_logs", required=False, default=False)

    def template_doc_printer(self) -> "TemplateDocPrinter":
        return TemplateDocPrinter(self.name, self.cli_command())


class TemplateProcessorTests(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()
        self.base = '/ccx-templates/python'

        self.fs.create_dir(f"{self.base}/package")
        self.resolver = TemplateResolver([self.base])

        self.template_processor = DummyTemplateProcessor('package', self.resolver)

    def tearDown(self) -> None:
        super().tearDown()

    def test_invalid_template(self):
        with self.assertRaises(Exception) as context:
            template_processor = DummyTemplateProcessor('package1', self.resolver)

        self.assertEqual("Template package1 not found", str(context.exception))

    def test_overwrite(self):
        self.assertFalse(self.template_processor._overwrite)
        self.assertIsInstance(self.template_processor.overwrite(True), DummyTemplateProcessor)
        self.assertTrue(self.template_processor._overwrite)

    def test_build_parser(self):
        self.assertIsNone(self.template_processor._parser)
        self.template_processor.build_parser()
        self.assertIsNotNone(self.template_processor._parser)

    def test_parse_with_required(self):
        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness",  # default value
            "logs": True,
            "extra_logs": False
        }
        var = self.template_processor.parse_arguments(['--app_name', "TheAwesomeApp"])
        self.assertDictEqual(expected, var)

    def test_parse_missing_required(self):
        with self.assertRaises(Exception) as context:
            self.template_processor.parse_arguments(['--app_description', "Awesomeness Unleashed"])

        self.assertEqual("the following arguments are required: --app_name", str(context.exception))

    def test_parse_optional_string(self):
        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness Unleashed",
            "logs": True,
            "extra_logs": False

        }
        var = self.template_processor.parse_arguments(
            ['--app_name', "TheAwesomeApp", '--app_description', "Awesomeness Unleashed"]
        )
        self.assertDictEqual(expected, var)

    def test_parse_optional_true_boolean(self):
        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness Unleashed",
            "logs": True,
            "extra_logs": False
        }
        var = self.template_processor.parse_arguments(
            ['--app_name', "TheAwesomeApp", '--app_description', "Awesomeness Unleashed", "--logs", "true"]
        )
        self.assertDictEqual(expected, var)

        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness Unleashed",
            "logs": False,
            "extra_logs": False
        }
        var = self.template_processor.parse_arguments(
            ['--app_name', "TheAwesomeApp", '--app_description', "Awesomeness Unleashed", "--logs", "false"]
        )
        self.assertDictEqual(expected, var)

    def test_parse_optional_false_boolean(self):
        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness Unleashed",
            "logs": True,
            "extra_logs": True
        }
        var = self.template_processor.parse_arguments(
            ['--app_name', "TheAwesomeApp", '--app_description', "Awesomeness Unleashed", "--extra_logs", "true"]
        )
        self.assertDictEqual(expected, var)

        expected = {
            "app_name": "TheAwesomeApp",
            "app_description": "Awesomeness Unleashed",
            "logs": True,
            "extra_logs": False
        }
        var = self.template_processor.parse_arguments(
            ['--app_name', "TheAwesomeApp", '--app_description', "Awesomeness Unleashed", "--extra_logs", "false"]
        )
        self.assertDictEqual(expected, var)

