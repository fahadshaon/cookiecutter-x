# Home

Cookiecutter eXtended is a code generator based on Jinja and Cookiecutter with some extra features.
Such as single file generation, local template management, template documentation,
provide template input using arguments instead of interactive prompts.


## Quick Start

- Install with pip - it will create a shell command `cookiecutter-x`.
    ```shell
    pip install cookiecutter-x
    ```
    - You _should_ create a separate virtual environment for this project.
    `virtualenvwrapper` is a great option for that.
    - Add the cli script `cookiecutter-x` into a `$PATH` dir. Assuming `$HOME/bin` is in `$PATH`
      ```shell
      ccx="$(which cookiecutter-x)" && ln -t $HOME/bin "$ccx"
      ```
    - More at [Installation](installation.md)

- Generate configurations (stored at `$HOME/.cookiecutter-x/ccx-config.yml`)
    ```shell
    cookiecutter-x quick-start config
    ```

- Add or write templates
  - Create a simple example template for generating CPP header and class pair
    ```shell
    cookiecutter-x quick-start example-template
    ```

- See the list of available simple templates
    ```shell
    cookiecutter-x simple list
    ```

- See the documentation of a template
    ```shell
    cookiecutter-x simple doc cpp
    ```

- Generate files based on a template
    ```shell
    cookiecutter-x simple process cpp --class_name 'FilesUtils'
    ```
