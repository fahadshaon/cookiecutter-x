import os.path

from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x.core import CCXConfig


class CCXConfigTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

        self.base_dir = os.path.join(os.path.expanduser('~'), CCXConfig.CCX_DIR_NAME)
        self.config_file = os.path.join(self.base_dir, CCXConfig.CCX_CONFIG_FILENAME)

        self.fs.create_file(self.config_file, contents='''
simple_templates:
  paths:
    - /ccx-templates/simple-templates

cookiecutter_templates:
  paths:
    - /ccx-templates/cookiecutter-templates/python
    - /ccx-templates/cookiecutter-templates/gradle

''')

        self.config = CCXConfig()

    def tearDown(self) -> None:
        super().tearDown()

    def test_template_paths(self):
        self.assertListEqual(['/ccx-templates/simple-templates'], self.config.simple_template_paths)
        self.assertSetEqual(
            {
                '/ccx-templates/cookiecutter-templates/python',
                '/ccx-templates/cookiecutter-templates/gradle'
            },
            set(self.config.cookiecutter_template_paths)
        )

    def test_single_path(self):
        self.fs.remove(self.config_file)
        self.fs.create_file(self.config_file, contents='''
simple_templates:
  paths: /ccx-templates/simple-templates
''')

        self.assertListEqual(['/ccx-templates/simple-templates'], self.config.simple_template_paths)

    def test_empty_config(self):
        self.fs.remove(self.config_file)
        self.fs.rmdir(self.base_dir)

        self.assertDictEqual({}, self.config.configs)

        self.assertListEqual([os.path.join(self.base_dir, 'simple-templates')], self.config.simple_template_paths)
        self.assertListEqual(
            [os.path.join(self.base_dir, 'cookiecutter-templates')],
            self.config.cookiecutter_template_paths
        )
