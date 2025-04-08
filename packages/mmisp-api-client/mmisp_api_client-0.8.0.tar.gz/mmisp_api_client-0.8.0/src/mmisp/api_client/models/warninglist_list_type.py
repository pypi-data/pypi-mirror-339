from enum import Enum


class WarninglistListType(str, Enum):
    CIDR = "cidr"
    HOSTNAME = "hostname"
    REGEX = "regex"
    STRING = "string"
    SUBSTRING = "substring"

    def __str__(self) -> str:
        return str(self.value)
