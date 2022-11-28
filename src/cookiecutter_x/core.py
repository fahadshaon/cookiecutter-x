import logging
import os
from typing import Dict, Any, List, Iterator, Tuple

import click
import yaml
from cached_property import cached_property


class CCXError(click.ClickException):
    def __init__(self, message, exit_code=-1):
        super().__init__(message)
        self.exit_code = exit_code

    def show(self, file=None):
        if file:
            super().show(file)
            return

        logging.error(self.message)


class CCXConfig:
    CCX_DIR_NAME = '.cookiecutter-x'
    CCX_CONFIG_FILENAME = 'ccx-config.yml'

    def __init__(self) -> None:
        super().__init__()
        self.base_path = os.path.join(os.path.expanduser('~'), self.CCX_DIR_NAME)
        self.configs_path = os.path.join(self.base_path, self.CCX_CONFIG_FILENAME)

    @cached_property
    def configs(self) -> Dict[str, Any]:
        if not os.path.exists(self.configs_path):
            return {}

        with open(self.configs_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, var_name: str) -> Any:
        if not var_name:
            raise CCXError('Must provide a variable name to search')

        cur = self.configs

        for v in var_name.split('.'):

            if v not in cur or cur is None:
                return None

            cur = cur[v]

        return cur

    def normalize_path(self, path: str) -> str:
        if path.startswith('~'):
            p = os.path.expanduser(path)

        elif not os.path.isabs(path):
            p = os.path.join(os.path.dirname(self.configs_path), path)
        else:
            p = path

        return os.path.normpath(p)

    def get_normalized_paths(self, config_key: str) -> List[str]:
        paths = self.get(config_key)
        if not paths:
            return []

        if isinstance(paths, str):
            paths = [paths]

        return sorted(self.normalize_path(p) for p in paths)

    @cached_property
    def simple_template_paths(self) -> List[str]:
        paths = self.get_normalized_paths("simple_templates.paths")
        if paths:
            return paths

        return [os.path.join(self.base_path, 'simple-templates')]

    def simple_template_resolver(self) -> "TemplateResolver":
        return TemplateResolver(self.simple_template_paths)

    @cached_property
    def cookiecutter_template_paths(self) -> List[str]:
        paths = self.get_normalized_paths("cookiecutter_templates.paths")

        if paths:
            return paths

        return [os.path.join(self.base_path, 'cookiecutter-templates')]

    def cookiecutter_template_resolver(self) -> "TemplateResolver":
        return TemplateResolver(self.cookiecutter_template_paths)


config = CCXConfig()


class TemplateResolver:
    def __init__(self, paths: List[str]) -> None:
        super().__init__()
        self.paths = paths

    def _iterate(self) -> Iterator[Tuple[str, str]]:
        for p in self.paths:
            if not os.path.exists(p):
                logging.warning(f"Template source path {p} not found; skipping")
                continue

            for t in os.listdir(p):
                yield t, os.path.join(p, t)

    def list(self) -> Dict[str, str]:
        return {name: path for name, path in self._iterate()}

    def get_path(self, name: str) -> str:
        for _name, path in self._iterate():
            if _name == name:
                return path

        raise CCXError(f"Template {name} not found")
