from datamodel_code_generator import DataModelType

from gadhttpclient import enums

MAPPING_PYTHON_MODULE_TO_DATAMODEL = {
    enums.PythonModule.pydantic: DataModelType.PydanticBaseModel,
    enums.PythonModule.dataclasses: DataModelType.DataclassesDataclass,
    enums.PythonModule.typing: DataModelType.TypingTypedDict,
    enums.PythonModule.msgspec: DataModelType.MsgspecStruct,
}
