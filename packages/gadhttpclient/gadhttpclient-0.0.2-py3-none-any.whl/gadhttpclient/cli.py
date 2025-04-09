import json
import shlex
import subprocess
from pathlib import Path

import typer
from datamodel_code_generator import DataModelType
from datamodel_code_generator import InputFileType
from datamodel_code_generator import generate as generate_models
from jinja2 import Template

from gadhttpclient import const
from gadhttpclient import enums
from gadhttpclient import mappers
from gadhttpclient import models
from gadhttpclient import parsers
from gadhttpclient.os import File
from gadhttpclient.os import Folder
from gadhttpclient.utils import paths
from gadhttpclient.utils import strings
from gadhttpclient.utils import temp

app = typer.Typer(help="gadhttpclient")


@app.command()
def generate(
    file: str = typer.Option(..., "-f", "--file", help="Path or link to configuration file"),
    context: str = typer.Option("{}", "-c", "--context", help="JSON context for templates"),
) -> None:
    cwd = paths.current()

    file, buffer = parsers.getconfig(file)

    config = strings.to_toml(File.read(file))

    if buffer:
        file.unlink(missing_ok=True)

    workdir = paths.define(config.get(const.SYNTAX_WORKDIR))

    Folder.create(workdir)

    context = json.loads(context)

    context["workdir"] = workdir

    clients = config.get(const.SYNTAX_CLIENTS, [])

    for client in clients:
        content = json.loads(parsers.getcontent(workdir=cwd, content=client.get(const.SYNTAX_CLIENTS_CONTENT)))

        if operations := client.get(const.SYNTAX_CLIENTS_OPERATIONS, []):
            content = parsers.filtercontent(content=content, operations=operations)

        if model := client.get(const.SYNTAX_CLIENTS_MODEL):
            module = enums.PythonModule(model)
        else:
            module = enums.PythonModule.pydantic

        schema = models.Specification(**content)

        path = workdir / Path(client.get(const.SYNTAX_CLIENTS_PATH))

        file, buffer = temp.getfile(str(content), extension=const.EXTENSION_JSON), True

        generate_models(
            file,
            output=path,
            input_file_type=InputFileType.OpenAPI,
            output_model_type=mappers.MAPPING_PYTHON_MODULE_TO_DATAMODEL.get(module),
            use_title_as_name=False,
        )

        if buffer:
            file.unlink(missing_ok=True)

        File.write(
            path=path,
            content=Template(File.read(Path(const.TEMPLATE_MODEL.format(module=module.name)))).render(),
            mode=const.FILE_APPEND,
        )

        File.write(
            path=path,
            content=Template(File.read(Path(const.TEMPLATE_CLIENT))).render(),
            mode=const.FILE_APPEND,
        )

        for url, route in schema.paths.items():
            for method in enums.HTTPMethod:
                if not (operation := getattr(route, method)):
                    continue

                function = parsers.parseoperation(operation)

                method = Template(File.read(Path(const.TEMPLATE_METHOD))).render(
                    {
                        "function": {
                            "async": client.get(const.SYNTAX_CLIENTS_ASYNC, True),
                            "name": operation.operationId,
                            "arguments": ", ".join(f"{arg.name}: {arg.annotation}" for arg in function.arguments),
                            "annotation": enums.TypingType.array.wrapp(function.options["response"]["name"])
                            if function.options["response"]["array"]
                            else function.options["response"]["name"],
                            "serialize": Template(
                                File.read(Path(const.TEMPLATE_MODEL_SERIALIZE.format(module=module.name)))
                            ).render(function.options["response"]),
                        },
                        "request": {
                            "method": method,
                            "url": url,
                            "paths": [
                                arg.name for arg in function.arguments if arg.location == enums.HTTPAttribute.path
                            ],
                            "params": {
                                arg.name: arg.name
                                for arg in function.arguments
                                if arg.location == enums.HTTPAttribute.query
                            },
                            "headers": {header.name: header.annotation for header in function.headers},
                            "json": function.options.get("body"),
                            "data": function.options.get("data"),
                            "file": function.options.get("file"),
                            "files": function.options.get("files"),
                            "auth": function.options.get("auth"),
                        },
                    }
                )

                File.write(path=path, content=const.SYMBOL_NEWLINE + method, mode=const.FILE_APPEND)

        File.write(path=path, content=strings.sortimports(File.read(path=path, tolist=True)))

    if scripts := config.get(const.SYNTAX_SCRIPTS, []):
        for script in scripts:
            if command := script.get(const.SYNTAX_SCRIPTS_COMMAND):
                subprocess.run(
                    shlex.split(Template(command).render(context)),
                    cwd=workdir,
                    text=True,
                    check=script.get(const.SYNTAX_SCRIPTS_CHECK, False),
                )


if __name__ == "__main__":
    app()
