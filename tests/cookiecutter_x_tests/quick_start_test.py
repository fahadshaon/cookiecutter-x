import os.path

from click.testing import CliRunner
from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x import quick_start
from cookiecutter_x.cli import cli
from cookiecutter_x.core import config


class QuickStartTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

    def tearDown(self) -> None:
        super().tearDown()

    def test_generate_config(self):
        runner = CliRunner()
        self.assertFalse(os.path.exists(config.configs_path))

        result = runner.invoke(cli, "quick-start config")

        self.assertEqual(0, result.exit_code)
        self.assertTrue(os.path.exists(config.configs_path))
        with open(config.configs_path) as f:
            self.assertEqual(quick_start.sample_config(), f.read())

    def test_generate_cpp_template(self):
        runner = CliRunner()
        cpp_template = os.path.join(config.simple_template_paths[0], 'cpp')
        self.assertFalse(os.path.exists(cpp_template))

        result = runner.invoke(cli, "quick-start sample-template")

        self.assertEqual(0, result.exit_code)
        self.assertTrue(os.path.exists(cpp_template))
        self.assertListEqual(['ccx.yml', 'cpp.cpp', 'cpp.h'], sorted(os.listdir(cpp_template)))

        contents = quick_start.ccp_template_content()

        with open (os.path.join(cpp_template, 'ccx.yml')) as f:
            self.assertEqual(contents['ccx'], f.read())

        with open (os.path.join(cpp_template, 'cpp.cpp')) as f:
            self.assertEqual(contents['cpp'], f.read())

        with open (os.path.join(cpp_template, 'cpp.h')) as f:
            self.assertEqual(contents['h'], f.read())
