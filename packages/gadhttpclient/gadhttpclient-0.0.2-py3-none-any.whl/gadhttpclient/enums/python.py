from enum import Enum


class PythonModule(str, Enum):
    pydantic = "pydantic"
    dataclasses = "dataclasses"
    typing = "typing"
    msgspec = "msgspec"


class PythonType(str, Enum):
    object = "dict"
    array = "list"
    string = "str"
    integer = "int"
    number = "float"
    boolean = "bool"
    null = "None"
    bytes = "bytes"
