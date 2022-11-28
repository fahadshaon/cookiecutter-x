# Installation

Like every other python package you can install `cookiecutter-x` with

```shell
pip install cookiecutter-x
```

This will create the executable console script `cookiecutter-x` in the bin directory.

## Creating and installing in virtualenv

Using [virtualenv wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) (this creates the virtual environments at `$HOME/.virtualenvs`)

```shell
mkvirtualenv cookiecutter-x -p /usr/bin/python3
workon cookiecutter-x
pip install cookiecutter-x
```

For installing a package in virtualenv using python3 provided venv package

```shell
python3 -m venv venv
. venv/bin/activate
pip install cookiecutter-x
```

## Executable

This package creates executable console script `cookiecutter-x`, which is automatically installed
inside the virtualenv's bin directory. You can link this script into a `PATH` directory.

Run the following with the virtualenv activated

```shell
ccx=$(which cookiecutter-x) && sudo ln -t /usr/local/bin $ccx
```

Now you can deactivate the virtualenv and will still be able to execute `cookiecutter-x` command.


## Autocomplete

CookiecutterX is built with python [click](https://click.palletsprojects.com) library.
So it is easy to create auto complete following instruction at <https://click.palletsprojects.com/en/8.0.x/shell-completion>.


=== "bash"

    ```shell
    _COOKIECUTTER_X_COMPLETE=bash_source cookiecutter-x > $HOME/.cookiecutter-x/cookiecutter-x.autocomplete.bash
    ```

    Source the file in `$HOME/.bashrc`.

    ```shell
    source $HOME/.cookiecutter-x/cookiecutter-x.autocomplete.bash
    ```

=== "zsh"

    ```shell
    _COOKIECUTTER_X_COMPLETE=zsh_source cookiecutter-x > $HOME/.cookiecutter-x/cookiecutter-x.autocomplete.zsh
    ```

    Source the file in `$HOME/.zshenv`.

    ```shell
    source $HOME/.cookiecutter-x/cookiecutter-x.autocomplete.zsh
    ```
