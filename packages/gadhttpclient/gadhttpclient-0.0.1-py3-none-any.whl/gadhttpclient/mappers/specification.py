from gadhttpclient import enums

MAPPING_TYPE_SPECIFICATION_TO_PYTHON = {
    enums.SpecificationSchemaType.object: enums.PythonType.object,
    enums.SpecificationSchemaType.array: enums.PythonType.array,
    enums.SpecificationSchemaType.string: enums.PythonType.string,
    enums.SpecificationSchemaType.integer: enums.PythonType.integer,
    enums.SpecificationSchemaType.number: enums.PythonType.number,
    enums.SpecificationSchemaType.boolean: enums.PythonType.boolean,
    enums.SpecificationSchemaType.null: enums.PythonType.null,
    (enums.SpecificationSchemaType.string, enums.SpecificationSchemaFormat.binary): enums.PythonType.bytes,
}
