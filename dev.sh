#!/usr/bin/env bash

set -euo pipefail

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function usage() {
    CMD="dev.sh"

    cat <<EOT
Helper script for development

Usage:
    ${CMD} help                 Print this message and quit
    ${CMD} install [-r]         Create virtualenv (venv) and install the project (editable)
    ${CMD} requirements         Generate the requirements.txt from current venv
    ${CMD} test                 Run unit tests
    ${CMD} coverage             Run coverages and generate html reports
    ${CMD} build                Build the binary

    ${CMD} docs-install [-r]    Create virtualenv (docs/venv) and install docs generation dependencies
    ${CMD} docs-requirements    Generate the requirements.txt from doc generation venv
    ${CMD} docs-build           Generate the docs using mkdocs
    ${CMD} docs-serve           Serve the mkdocs

** All the commands run from project root (SCRIPT_PATH)
EOT
}

function py_bins_path() {
    if [[ ${1-} == "app" ]]; then
        venv="venv"
        requirements="requirements.txt"
    elif [[ ${1-} == "docs" ]]; then
        venv="docs/venv"
        requirements="docs/requirements.txt"
    else
        echo "Invalid virtualenv type"
        exit 1
    fi

    python_bin="${venv}/bin/python3"
    pip_bin="${venv}/bin/pip"
}

function create_virtual_env() {
    py_bins_path "$1"

    echo "Installing Cookiecutter-X for development"

    if [[ -x $python_bin ]]; then
        echo "Python binary found inside the virtualenv directory"
    else
        echo "Creating virtualenv ${venv}"
        python3 -m venv "${venv}"
    fi

    echo "Installing latest version of pip, wheel, and build"
    "${pip_bin}" install -U pip wheel build

    if [[ ${2-} == '-r' ]]; then
        echo "Installing requirements ${requirements} in ${venv}"
        "${pip_bin}" install -r "${requirements}"
    fi

    if [[ ${1-} == "app" ]]; then
        # Installing the project in editable mode with test requirements
        "${pip_bin}" install -e ".[test]"
    fi
}

function cmd-install() {
    create_virtual_env "app" "$@"
}

function create_requirements() {
    py_bins_path "$1"

    echo "Creating requirements file"
    "$pip_bin" freeze | grep -e '#' -e "cookiecutter-x" -e 'pkg-resources==0.0.0' -e "pkg_resources==0.0.0" -v >"$requirements"
}

function cmd-requirements() {
    create_requirements "app"
}

function cmd-test() {
    echo "Running unittests"
    venv/bin/python3 -m unittest discover -s "tests" -v -p '*_test.py'
}

function cmd-coverage() {
    echo "Running coverage"
    venv/bin/coverage run -m unittest discover -s tests -v -p '*_test.py'

    echo 'Running coverage report'
    venv/bin/coverage report -m

    echo 'Generating coverage html report'
    venv/bin/coverage html

    venv/bin/python3 -m unittest discover -s "tests" -v -p '*_test.py'
}

function cmd-build() {
    echo "Building the binary"
    venv/bin/python3 -m build
}

function cmd-docs-install() {
    if [[ -z $* ]]; then
        create_virtual_env "docs"
        docs/venv/bin/pip install mkdocs mkdocs-material mkdocs-awesome-pages-plugin
    else
        create_virtual_env "docs" $@
    fi
}

function cmd-docs-requirements() {
    create_requirements "docs"
}

function cmd-docs-build() {
    pushd docs >/dev/null || exit 1

    venv/bin/mkdocs build "$@"

    popd >/dev/null || exit 1
}

function cmd-docs-serve() {
    pushd docs >/dev/null || exit 1

    venv/bin/mkdocs serve "$@"

    popd >/dev/null || exit 1
}

if [[ -z "$*" || "$1" == '-h' || "$1" == '--help' || "$1" == 'help' ]]; then
    usage
    exit 0
fi

command="cmd-${1}"

if [[ $(type -t "${command}") != "function" ]]; then
    echo "Error: No command found"
    usage
    exit 1
fi

# All the commands run from the project root
pushd "$SCRIPT_PATH" >/dev/null || exit 1

${command} "${@:2}"

popd >/dev/null || exit 1
