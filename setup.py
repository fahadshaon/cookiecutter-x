import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cookiecutter-x",
    version="0.1.2",
    description="Cookiecutter eXtended",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='cookiecutter-x, cookiecutter, projects, project templates, Jinja2, scaffolding, development',

    author="Fahad Shaon",
    author_email="fs@shaon.dev",

    url="https://github.com/fahadshaon/cookiecutter-x",
    project_urls={
        "Bug Tracker": "https://github.com/fahadshaon/cookiecutter-x/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    py_modules=['cookiecutter_x'],
    install_requires=[
        'cached-property',
        'cookiecutter',
        'click',
        'coloredlogs',
        'Jinja2',
        'PyYaml',
        'tabulate'
    ],
    extras_require={
        'test': ['coverage', 'pyfakefs'],
    },
    entry_points='''
        [console_scripts]
        cookiecutter-x=cookiecutter_x.main:main
    ''',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
