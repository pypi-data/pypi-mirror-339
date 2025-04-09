from enum import Enum
from typing import Optional


class TypingType(str, Enum):
    array = "List"
    union = "Union"
    null = "Optional"
    any = "Any"

    def wrapp(self, annotation: Optional[str] = None) -> str:
        if self in (self.array, self.union):
            return f"{self.value}[{annotation}]"
        elif self is self.null:
            return f"{self.value}[{annotation}] = None"
        else:
            return self.value
