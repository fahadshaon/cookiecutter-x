import logging

from pyfakefs.fake_filesystem_unittest import TestCase

from cookiecutter_x.core import TemplateResolver


class TemplateResolverTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

        self.base = '/ccx-templates/python'
        self.fs.create_dir(f"{self.base}/package_structure1")
        self.fs.create_dir(f"{self.base}/package_structure2")

        self.resolver = TemplateResolver([self.base])

    def tearDown(self) -> None:
        super().tearDown()

    def test_list(self):
        self.assertDictEqual(
            {
                'package_structure1': '/ccx-templates/python/package_structure1',
                'package_structure2': '/ccx-templates/python/package_structure2'
            }, self.resolver.list()
        )

    def test_get_path(self):
        self.assertEqual('/ccx-templates/python/package_structure1', self.resolver.get_path('package_structure1'))
        self.assertEqual('/ccx-templates/python/package_structure2', self.resolver.get_path('package_structure2'))

    def test_get_path_fails(self):
        with self.assertRaises(Exception) as context:
            self.resolver.get_path('random')

        self.assertEqual("Template random not found", str(context.exception))


class TemplateResolverTestIgnorePaths(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.setUpPyfakefs()

    def tearDown(self) -> None:
        super().tearDown()

    @classmethod
    def setUpClass(cls):
        super(TemplateResolverTestIgnorePaths, cls).setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        super(TemplateResolverTestIgnorePaths, cls).tearDownClass()
        logging.disable(logging.NOTSET)

    def test_invalid_dir(self):
        python = '/ccx-templates/python'
        gradle = '/ccx-templates/gradle'
        self.fs.create_dir(f"{python}/package_structure1")
        self.fs.create_dir(f"{python}/package_structure2")

        resolver = TemplateResolver([python, gradle])

        self.assertDictEqual(
            {
                'package_structure1': '/ccx-templates/python/package_structure1',
                'package_structure2': '/ccx-templates/python/package_structure2'
            }, resolver.list()
        )
