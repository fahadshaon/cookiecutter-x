import os
import re
from datetime import datetime

from jinja2.ext import Extension


class CCXExtension(Extension):
    """Jinja2 extension for adding simple text manipulation filters and utility methods"""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super(CCXExtension, self).__init__(environment)

        def snake_case(val: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', val)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        def remove_extension(val: str) -> str:
            if '.' not in val:
                return val

            return os.path.splitext(val)[0]

        def java_package_to_dir(val: str) -> str:
            if val.startswith('.'):
                raise ValueError("Java package shouldn't start with '.'")

            return val.strip().replace('.', '/')

        environment.filters['snake_case'] = snake_case
        environment.filters['remove_extension'] = remove_extension
        environment.filters['java_package_to_dir'] = java_package_to_dir

        environment.globals['n'] = datetime.now
