"""
Specification
├── openapi
├── info
│   ├── title
│   ├── description
│   └── version
├── paths
│   ├── <path>
│   │   ├── get
│   │   ├── post
│   │   ├── put
│   │   ├── patch
│   │   └── delete
│   │       ├── tags
│   │       ├── summary
│   │       ├── operationId
│   │       ├── parameters
│   │       │   ├── name
│   │       │   ├── in
│   │       │   ├── required
│   │       │   ├── description
│   │       │   └── schema
│   │       │       └── Schema | Reference
│   │       ├── requestBody
│   │       │   ├── required
│   │       │   └── content
│   │       │       └── <content-type>
│   │       │           └── schema
│   │       │               └── Schema | Reference
│   │       ├── responses
│   │       │   ├── <status-code>
│   │       │   │   ├── description
│   │       │   │   └── content
│   │       │   │       └── <content-type>
│   │       │   │           └── schema
│   │       │   │               └── Schema | Reference
│   │       └── security
├── components
│   └── schemas
│       └── <name>
│           ├── title
│           ├── type
│           ├── format
│           ├── enum
│           ├── description
│           ├── default
│           ├── properties
│           │   └── <name>: Schema | Reference
│           ├── required
│           ├── items
│           │   └── Schema | Reference
│           ├── allOf | anyOf | oneOf
│           │   └── List[Schema | Reference]
│           └── additionalProperties
│               └── bool | Schema | Reference
└── security
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field

from gadhttpclient import const
from gadhttpclient import enums


class SpecificationReference(BaseModel):
    ref: str = Field(..., alias="$ref")

    @classmethod
    def name(cls, value: str) -> str:
        return value.split(const.SYMBOL_FORWARD_SLASH)[-1]


class SpecificationSchema(BaseModel):
    title: Optional[str] = None
    type: Optional[enums.SpecificationSchemaType] = None
    format: Optional[enums.SpecificationSchemaFormat] = None
    enum: Optional[List[Any]] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    properties: Optional[Dict[str, Union[SpecificationSchema, SpecificationReference]]] = None
    required: Optional[List[str]] = None
    items: Optional[Union[SpecificationSchema, SpecificationReference]] = None
    allOf: Optional[List[Union[SpecificationSchema, SpecificationReference]]] = None
    anyOf: Optional[List[Union[SpecificationSchema, SpecificationReference]]] = None
    oneOf: Optional[List[Union[SpecificationSchema, SpecificationReference]]] = None
    additionalProperties: Optional[Union[bool, SpecificationSchema, SpecificationReference]] = None


class SpecificationContent(BaseModel):
    model: Optional[Union[SpecificationSchema, SpecificationReference]] = Field(None, alias="schema")


class SpecificationPathOperationParameter(BaseModel):
    name: str
    location: enums.HTTPAttribute = Field(..., alias="in")
    required: Optional[bool] = None
    description: Optional[str] = None
    model: Optional[Union[SpecificationSchema, SpecificationReference]] = Field(..., alias="schema")


class SpecificationPathOperationRequestBody(BaseModel):
    required: Optional[bool] = None
    content: Dict[enums.HTTPContentType, SpecificationContent]


class SpecificationPathOperationResponse(BaseModel):
    description: Optional[str] = None
    content: Optional[Dict[enums.HTTPContentType, SpecificationContent]] = None


class SpecificationPathOperation(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    operationId: str
    parameters: Optional[List[Union[SpecificationPathOperationParameter, SpecificationReference]]] = None
    requestBody: Optional[Union[SpecificationPathOperationRequestBody, SpecificationReference]] = None
    responses: Dict[HTTPStatus, SpecificationPathOperationResponse]
    security: Optional[List[Dict[enums.SpecificationSecurityType, List[str]]]] = None


class SpecificationPath(BaseModel):
    get: Optional[SpecificationPathOperation] = None
    post: Optional[SpecificationPathOperation] = None
    put: Optional[SpecificationPathOperation] = None
    patch: Optional[SpecificationPathOperation] = None
    delete: Optional[SpecificationPathOperation] = None


class SpecificationInfo(BaseModel):
    title: str
    description: Optional[str] = None
    version: str


class SpecificationComponents(BaseModel):
    schemas: Optional[Dict[str, Union[SpecificationSchema, SpecificationReference]]] = None


class Specification(BaseModel):
    openapi: str
    info: SpecificationInfo
    paths: Dict[str, SpecificationPath]
    components: Optional[SpecificationComponents] = None
    security: Optional[List[Dict[enums.SpecificationSecurityType, List[str]]]] = None
