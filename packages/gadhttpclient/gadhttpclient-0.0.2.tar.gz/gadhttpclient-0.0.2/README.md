<p align="center">
  <a href="https://github.com/AlexDemure/gadhttpclient">
    <a href="https://ibb.co/XfKN0Dns"><img src="https://i.ibb.co/7xZ8MQ3W/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A CLI tool that generates HTTP clients from an OpenAPI specification.
</p>

---

## Installation

```
pip install gadhttpclient
```

## Usage

Run the code generation process:

```sh
gadhttpclient --file {config.toml} --context "{}"
```


## Configuration File Guide

gadhttpclient uses a structured TOML configuration file.

### General Structure

```
workdir = "myproject"

[[clients]]
path = "{{name}}.py"
content = "file:openapi.json"
model = "pydantic"
async = true
operations = []

[[scripts]]
command = "isort {{workdir}}"
check = true
```

### Sections Overview

| Section       | Format                               | Description                                                              |   |   |
|---------------|--------------------------------------|--------------------------------------------------------------------------|---|---|
| `workdir`     | `""`                                 | Uses the current directory                                               |   |   |
|               | `"myproject"`                        | Uses the current directory + `/myproject`                                |   |   |
|               | `"/home/myproject"`                  | Uses an absolute path                                                    |   |   |
| `[[clients]]` |                                      | Defines file creation rules                                              |   |   |
|               | `mode = "a"`                         | File writing mode: `"a"` (append), `"w"` (overwrite)                     |   |   |
|               | `path = "src/__init__.py"`           | Relative to workdir, specifies file location.                            |   |   |
|               | `content = """ ... """ / path / url` | Raw content, local file path, or URL for remote content.                 |   |   |
|               | `model = "pydantic"`                 | Type of models created                                                   |   |   |
|               | `async = "true"`                     | Type of methods                                                          |   |   |
|               | `operations = []`                    | Filtering methods by operation_id                                        |   |   |
| `[[scripts]]` |                                      | Defines commands to be executed after generation.                        |   |   |
|               | `command = "isort {{workdir}}"`      | Command to execute, supports dynamic variables.                          |   |   |
|               | `check = True\False"`                | If true, raises an error if the command fails, otherwise logs output.    |   |   |


## Using Dynamic Variables

gadhttpclient supports dynamic variables in both file paths, contents, and script commands.

```toml
[[clients]]
path = "src/{{name}}.py
```

## Automating Post-Generation Tasks

gadhttpclient allows you to execute scripts after generating files. These scripts can perform tasks such as formatting, linting, or additional file modifications.

#### Example
```
[[scripts]]
command = "isort {{workdir}}"
check = true

[[scripts]]
command = "ruff {{workdir}} --fix"
check = false
```

- Commands support dynamic variables.
- If check = true, the execution will fail if the command returns a non-zero exit code.
