from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel, Field

from gadhttpclient import enums


class HTTPProperty(BaseModel):
    name: str
    annotation: str
    location: enums.HTTPAttribute
    required: bool


class HTTPFunction(BaseModel):
    arguments: List[HTTPProperty]
    headers: List[HTTPProperty]
    options: Dict[str, Any] = Field(default_factory=dict)
