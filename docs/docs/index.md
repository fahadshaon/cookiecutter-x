# Home

Cookiecutter eXtended is a code generator based on Jinja and Cookiecutter with some extra features.
Such as single file generation, local template management, template documentation,
provide template input using arguments instead of interactive prompts.


## Quick Start

- Install with pip - it will create a shell command `cookiecutter-x`.
    ```shell
    pip install cookiecutter-x
    ```

- (Optional) add autocomplete for bash add `.bashrc` or any other profile file
    ```shell
    eval "$(_COOKIECUTTER_X_COMPLETE=bash_source cookiecutter-x)"`
    ```

- Generate configurations (stored at `$HOME/.cookiecutter-x/ccx-config.yml`)
    ```shell
    cookiecutter-x generate-config
    ```

- Add or write templates
  - Add sample template
    ```shell
    cookiecutter-x generate-sample
    ```

- See the list of available simple templates
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
