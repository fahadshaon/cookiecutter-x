# Cookiecutter-X

Cookiecutter eXtended is a code generator based on Jinja and Cookiecutter with some extra features.
Such as single file generation, local template management, template documentation,
provide template input using arguments instead of interactive prompts.

## Installation

Like every other python package, you can install `cookiecutter-x` with

```shell
pip install cookiecutter-x
```

It will create the executable console script `cookiecutter-x` in the bin directory.

## Templates

Cookiecutter-X supports two types of templates.

- **Simple template**, optimized for generating standalone script(s), e.g. a bash script.
- **Cookiecutter template**, optimized for starting a new project, e.g., a python project


## Getting started quickly

- Generate configurations (stored at `$HOME/.cookiecutter-x/ccx-config.yml`)
    ```shell
    cookiecutter-x generate-config
    ```

- Add or write templates
  - Add sample template
    ```shell
    cookiecutter-x add-samples
    ```

- See a list of available simple templates
    ```shell
    cookiecutter-x sample list
    ```

- See the documentation of a template
    ```shell
    cookiecutter-x sample doc cpp
    ```

- Generate files based on a template
    ```shell
    cookiecutter-x sample process cpp --class_name 'FilesUtils'
    ```

Read more at the documentation site - <https://cookiecutter-x.shaon.dev>
