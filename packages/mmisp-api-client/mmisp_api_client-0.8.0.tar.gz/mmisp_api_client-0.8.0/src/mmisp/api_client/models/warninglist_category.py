from enum import Enum


class WarninglistCategory(str, Enum):
    FALSE_POSITIVE = "False positive"
    KNOWN_IDENTIFIER = "Known identifier"

    def __str__(self) -> str:
        return str(self.value)
