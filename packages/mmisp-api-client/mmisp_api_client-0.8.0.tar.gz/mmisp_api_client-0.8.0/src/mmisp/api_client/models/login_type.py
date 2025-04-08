from enum import Enum


class LoginType(str, Enum):
    IDP = "idp"
    PASSWORD = "password"

    def __str__(self) -> str:
        return str(self.value)
