# Configurations

CookiecutterX reads configurations from `$HOME/.cookiecutter-x/ccx-config.yml` file.
As sample configurations look

```yaml
simple_templates:
  paths:
    - ~/.cookiecutter-x/simple-templates

cookiecutter_templates:
  paths:
    - ~/.cookiecutter-x/cookiecutter-templates
```

CookiecutterX looks for a template directory inside these directories. For example, a simple template `cpp`
should be inside one of the directories mentioned in the`simple_templates.paths` list.

If no paths are provided cookiecutter-x reads templates from `$HOME/.cookiecutter-x/simple_templates`
and `$HOME/.cookiecutter-x/cookiecutter-templates` path.
