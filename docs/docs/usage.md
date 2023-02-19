# Usage

The `cookiecutter-x` CLI has three main groups of commands
- `quick-start`  Generate example configuration and template
- `simple` - Manage and process simple templates
- `cc` - Manage and process simple templates

## Generate configurations and template generation

Generate configuration

```shell
cookiecutter-x quick-start config
```

Generate the example simple template, i.e., the c++ header-implementation pair template

```shell
cookiecutter-x quick-start example-template
```

## Template processing commands

The `simple` and `cc` command groups have these commands.

- `list` - Lists all available templates
- `doc` - Print information of a template with variables and CLI command
- `process` - Process the template with input arguments

### `list` - Prints list of templates


```shell
$ cookiecutter-x simple list
```

### `doc` - Print template documentation

```shell
$ cookiecutter-x simple doc <template-name>
```

Applied on our example `cpp` template

```text
$ cookiecutter-x simple doc cpp

cpp
---
Generate CPP and H with include protection

Variables
---------
- class_name (required)

Run
---
    cookiecutter-x simple process cpp --class_name '<value>'
```

### `process` - Generate files using the template

```shell
$ cookiecutter-x simple process <template-name> [arguments]
```

Process the template with

```text
cookiecutter-x simple process cpp --class_name Awesomeness
```
