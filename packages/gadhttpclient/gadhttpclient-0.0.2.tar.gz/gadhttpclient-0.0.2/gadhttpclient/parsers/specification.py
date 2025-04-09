from http import HTTPStatus
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from gadhttpclient import const
from gadhttpclient import enums
from gadhttpclient import mappers
from gadhttpclient import models
from gadhttpclient.os import HTTP
from gadhttpclient.os import File
from gadhttpclient.utils import strings
from gadhttpclient.utils import urls


def getcontent(workdir: Path, content: str) -> str:
    if content.startswith(const.SYNTAX_FILE):
        path = Path(content[len(const.SYNTAX_FILE) :].strip())

        if not path.is_absolute():
            path = workdir / path

        if path.exists() and path.is_file():
            return File.read(path)

    elif urls.checkurl(content):
        return HTTP.download(content)

    return content


def filtercontent(content: dict, operations: list[str]) -> dict:
    paths = content.get(const.SPECIFICATION_PATHS, {})
    refs = set()

    for path, methods in list(paths.items()):
        for method, operation in list(methods.items()):
            if (
                not isinstance(operation, dict)
                or operation.get(const.SPECIFICATION_PATH_OPERATION_ID) not in operations
            ):
                del methods[method]
                continue

            stack = [operation]
            while stack:
                current = stack.pop()
                if not isinstance(current, dict):
                    continue
                for key, value in current.items():
                    if key == "$ref" and isinstance(value, str):
                        refs.add(value)
                    elif isinstance(value, dict):
                        stack.append(value)
                    elif isinstance(value, list):
                        stack.extend(x for x in value if isinstance(x, dict))

        if not methods:
            del paths[path]

    if components := content.get(const.SPECIFICATION_COMPONENTS, {}):
        if schemas := components.get(const.SPECIFICATION_COMPONENTS_SCHEMAS, {}):
            names = {models.SpecificationReference.name(ref) for ref in refs}
        content[const.SPECIFICATION_COMPONENTS][const.SPECIFICATION_COMPONENTS_SCHEMAS] = {
            k: v for k, v in schemas.items() if k in names
        }

    return content


def parsename(schema: models.SpecificationReference) -> str:
    return strings.to_pascal(schema.name(schema.ref))


def parsetype(schema: Union[models.SpecificationSchema, models.SpecificationReference]) -> str:
    if isinstance(schema, models.SpecificationReference):
        return parsename(schema)

    if schema.items:
        return enums.TypingType.array.wrapp(parsetype(schema.items))

    if schema.format == enums.SpecificationSchemaFormat.binary:
        return mappers.MAPPING_TYPE_SPECIFICATION_TO_PYTHON[(schema.type, schema.format)].value
    else:
        return mappers.MAPPING_TYPE_SPECIFICATION_TO_PYTHON[schema.type].value


def parseschema(schema: models.SpecificationSchema) -> str:
    return (
        const.SYMBOL_EMPTY
        if isinstance(schema, models.SpecificationSchema) and schema.type == enums.SpecificationSchemaType.null
        else parsetype(schema)
    )


def parseof(schema: models.SpecificationSchema) -> str:
    schemas, is_null = [], False

    for schema in schema.anyOf or schema.oneOf or schema.allOf:
        if schema := parseschema(schema):
            schemas.append(schema)
        else:
            is_null = True

    annotation = ", ".join(schemas)

    if len(schemas) > 1:
        annotation = enums.TypingType.union.wrapp(annotation)

    if is_null:
        annotation = enums.TypingType.null.wrapp(annotation)

    return annotation


def parsemodel(schema: Union[models.SpecificationSchema, models.SpecificationReference]) -> str:
    if isinstance(schema, models.SpecificationReference):
        return parsename(schema)
    if schema.anyOf or schema.oneOf or schema.allOf:
        return parseof(schema)
    return parseschema(schema)


def parseparams(parameters: List[models.SpecificationPathOperationParameter]) -> models.HTTPFunction:
    arguments, headers = [], []

    for parameter in parameters:
        name = strings.to_snake(parameter.name)
        annotation = parsemodel(parameter.model)
        required = parameter.required if parameter.required is not None else False

        if parameter.location == enums.HTTPAttribute.path:
            required = True

        if not required:
            if not annotation.startswith(enums.TypingType.null.value):
                annotation = enums.TypingType.null.wrapp(annotation)

        argument = models.HTTPProperty(
            name=name,
            annotation=annotation,
            location=parameter.location,
            required=required,
        )

        if parameter.location == enums.HTTPAttribute.header:
            headers.append(
                models.HTTPProperty(
                    name=parameter.name,
                    annotation=name,
                    location=parameter.location,
                    required=required,
                )
            )

        arguments.append(argument)

    return models.HTTPFunction(arguments=arguments, headers=headers)


def parsesecurity(security: List[Dict[enums.SpecificationSecurityType, List[str]]]) -> models.HTTPFunction:
    arguments, headers, options = [], [], {}

    for sec in security:
        for type, _ in sec.items():
            if type == enums.SpecificationSecurityType.bearer:
                arguments.append(
                    models.HTTPProperty(
                        name=const.HTTP_BEARER_KEY,
                        annotation=enums.PythonType.string.value,
                        location=enums.HTTPAttribute.header,
                        required=True,
                    )
                )
                headers.append(
                    models.HTTPProperty(
                        name=const.HTTP_BEARER_HEADER,
                        annotation=const.HTTP_BEARER_VALUE,
                        location=enums.HTTPAttribute.header,
                        required=True,
                    )
                )
            elif type == enums.SpecificationSecurityType.basic:
                arguments.append(
                    models.HTTPProperty(
                        name=const.HTTP_BASIC_USERNAME,
                        annotation=enums.PythonType.string.value,
                        location=enums.HTTPAttribute.header,
                        required=True,
                    )
                )
                arguments.append(
                    models.HTTPProperty(
                        name=const.HTTP_BASIC_PASSWORD,
                        annotation=enums.PythonType.string.value,
                        location=enums.HTTPAttribute.header,
                        required=True,
                    )
                )
                options[const.HTTP_BASIC_KEY] = True

    return models.HTTPFunction(arguments=arguments, headers=headers, options=options)


def parserequest(request: models.SpecificationPathOperationRequestBody) -> models.HTTPFunction:
    arguments, headers, options = [], [], {}

    required = request.required if request.required is not None else False

    for content_type, content in request.content.items():
        model = parsemodel(content.model)

        if not required:
            if not model.startswith(enums.TypingType.null.value):
                model = enums.TypingType.null.wrapp(model)

        if content_type is enums.HTTPContentType.json:
            arguments.append(
                models.HTTPProperty(
                    name=const.HTTP_CONTENT_BODY,
                    annotation=model,
                    location=enums.HTTPAttribute.body,
                    required=required,
                )
            )
            headers.append(
                models.HTTPProperty(
                    name=const.HTTP_CONTENT_TYPE_HEADER,
                    annotation=content_type,
                    location=enums.HTTPAttribute.header,
                    required=True,
                )
            )
            options[const.HTTP_CONTENT_BODY] = True

        elif content_type is enums.HTTPContentType.multipart:
            files = False

            if isinstance(content.model, models.SpecificationSchema):
                if content.model.type == enums.SpecificationSchemaType.array:
                    files = True

            name = const.HTTP_CONTENT_FILES if files else const.HTTP_CONTENT_FILE
            annotation = (
                enums.TypingType.array.wrapp(const.HTTP_CONTENT_FILE_MODEL) if files else const.HTTP_CONTENT_FILE_MODEL
            )

            if not required:
                annotation = enums.TypingType.null.wrapp(annotation)

            arguments.append(
                models.HTTPProperty(
                    name=name,
                    annotation=annotation,
                    location=enums.HTTPAttribute.body,
                    required=required,
                )
            )
            headers.append(
                models.HTTPProperty(
                    name=const.HTTP_CONTENT_TYPE_HEADER,
                    annotation=enums.HTTPContentType.multipart,
                    location=enums.HTTPAttribute.header,
                    required=True,
                )
            )
            options[name] = True

        elif content_type is enums.HTTPContentType.form:
            arguments.append(
                models.HTTPProperty(
                    name=const.HTTP_CONTENT_DATA, annotation=model, location=enums.HTTPAttribute.body, required=required
                )
            )
            headers.append(
                models.HTTPProperty(
                    name=const.HTTP_CONTENT_TYPE_HEADER,
                    annotation=enums.HTTPContentType.form,
                    location=enums.HTTPAttribute.header,
                    required=True,
                )
            )
            options[const.HTTP_CONTENT_DATA] = True

    return models.HTTPFunction(arguments=arguments, headers=headers, options=options)


def parseresponses(responses: Dict[HTTPStatus, models.SpecificationPathOperationResponse]) -> models.HTTPFunction:
    array = False
    name = None

    for status in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
        if response := responses.get(status):
            if content := response.content:
                for _, schema in content.items():
                    if model := schema.model:
                        if not (isinstance(model, models.SpecificationSchema) and model.type is None):
                            model = parsemodel(model)
                            if model.startswith(enums.TypingType.array.value):
                                array = True
                                if not model[5:-1] in {e.value for e in enums.PythonType}:
                                    name = model[5:-1]
                            elif model not in {e.value for e in enums.PythonType}:
                                name = model

    return models.HTTPFunction(
        arguments=[],
        headers=[],
        options=dict(
            response=dict(
                name=name,
                array=array,
                python=name in {e.value for e in enums.PythonType},
            )
        ),
    )


def parseoperation(operation: models.SpecificationPathOperation) -> models.HTTPFunction:
    security, parameters, request, response = None, None, None, None
    arguments, headers = [], []
    options = {}

    if operation.security:
        security = parsesecurity(operation.security)

    if operation.parameters:
        parameters = parseparams(operation.parameters)

    if operation.requestBody:
        request = parserequest(operation.requestBody)

    response = parseresponses(operation.responses)

    if security:
        arguments.extend(security.arguments)
        headers.extend(security.headers)
        # print(security.options)
        options.update(security.options or {})

    if parameters:
        arguments.extend([arg for arg in parameters.arguments if arg.location == enums.HTTPAttribute.path])
        arguments.extend(
            [arg for arg in parameters.arguments if arg.location == enums.HTTPAttribute.query and arg.required]
        )
        headers.extend(parameters.headers)

    if request:
        arguments.extend(request.arguments)
        headers.extend(request.headers)
        options.update(request.options or {})

    if parameters:
        arguments.extend(
            [arg for arg in parameters.arguments if arg.location == enums.HTTPAttribute.query and not arg.required]
        )

    options.update(response.options)

    return models.HTTPFunction(arguments=arguments, headers=headers, options=options)
