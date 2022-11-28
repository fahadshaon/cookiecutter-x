# Templates in CookiecutterX

Cookiecutter-x supports two types of templates.

- **Simple template**, optimized for generating standalone script(s), e.g., a bash script.
- **Cookiecutter template**, optimized for starting a new project, e.g., a python project.

## Simple template

Simple templates are ideal for creating a single file or a few files, such as a bash script, a c++ header-implementation pair files.

We write the template definition in `ccx.yml` with the following attributes.

- `name` - string
- `descirption` - string
- `variables` - map of variables, each containing `required` (boolean), `type` (string), `default` (boolean|string|number)
- `files` - list  of files to generate, each containing `name` (name of the template file) and `output` (output name of the file, this can be a jinja template)

For example, let's create a template to generate `.h` and `.cpp` for a class. The file structure is

```text
simple-templates/
└── cpp
    ├── ccx.yml
    ├── cpp.cpp
    └── cpp.h
```
Note: we configured the path to `simple-templates` directory in `simple_templates.paths` list in the config file (`$HOME/.cookiecutter-x/ccx-config.yml`).

Content of `cpp/ccx.yml`

```yaml
name: cpp
description: Generate CPP and H with include protection

variables:
  class_name:
    required: true
    type: string

files:
  - name: cpp.cpp
    output: "{{ class_name | remove_extension }}.cpp"
  - name: cpp.h
    output: "{{ class_name | remove_extension }}.h"
```

Content of `cpp/cpp.cpp`

```c
#include "{{ class_name | remove_extension }}.h"
```

Content of `cpp/cpp.h`

```cpp
#ifndef __{{ class_name | remove_extension | snake_case | upper }}_H__
#define __{{ class_name | remove_extension | snake_case | upper }}_H__

class {{class_name}} {

public:
    virtual void action();
};

#endif
```

## Cookiecutter templates

All cookiecutter templates work without any modifications. In addition, you can provide extra information (such as `description`, `post_gen` message) in `ccx.yml`.
