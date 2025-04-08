from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MiscellaneousGraphValidationError")


@_attrs_define
class MiscellaneousGraphValidationError:
    """Validation errors that do no fit in the legacy MISP json response format for Graph Validation will be returned as
    errors in this format.

        Attributes:
            error_id (str):
            message (str):
    """

    error_id: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_id = self.error_id

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error_id": error_id,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error_id = d.pop("error_id")

        message = d.pop("message")

        miscellaneous_graph_validation_error = cls(
            error_id=error_id,
            message=message,
        )

        miscellaneous_graph_validation_error.additional_properties = d
        return miscellaneous_graph_validation_error

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
