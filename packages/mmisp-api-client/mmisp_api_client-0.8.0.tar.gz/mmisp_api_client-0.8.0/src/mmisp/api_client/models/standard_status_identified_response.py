from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="StandardStatusIdentifiedResponse")


@_attrs_define
class StandardStatusIdentifiedResponse:
    """
    Attributes:
        name (str):
        message (str):
        url (str):
        saved (bool):
        success (bool):
        id (int):
    """

    name: str
    message: str
    url: str
    saved: bool
    success: bool
    id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        message = self.message

        url = self.url

        saved = self.saved

        success = self.success

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "message": message,
                "url": url,
                "saved": saved,
                "success": success,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        message = d.pop("message")

        url = d.pop("url")

        saved = d.pop("saved")

        success = d.pop("success")

        id = d.pop("id")

        standard_status_identified_response = cls(
            name=name,
            message=message,
            url=url,
            saved=saved,
            success=success,
            id=id,
        )

        standard_status_identified_response.additional_properties = d
        return standard_status_identified_response

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
