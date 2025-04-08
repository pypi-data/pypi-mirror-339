from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditUserRoleResponse")


@_attrs_define
class EditUserRoleResponse:
    """
    Attributes:
        saved (bool):
        name (str):
        message (str):
        url (str):
        id (int):
        success (Union[Unset, bool]):
        role (Union[Unset, str]):
    """

    saved: bool
    name: str
    message: str
    url: str
    id: int
    success: Union[Unset, bool] = UNSET
    role: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        name = self.name

        message = self.message

        url = self.url

        id = self.id

        success = self.success

        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "saved": saved,
                "name": name,
                "message": message,
                "url": url,
                "id": id,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if role is not UNSET:
            field_dict["Role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saved = d.pop("saved")

        name = d.pop("name")

        message = d.pop("message")

        url = d.pop("url")

        id = d.pop("id")

        success = d.pop("success", UNSET)

        role = d.pop("Role", UNSET)

        edit_user_role_response = cls(
            saved=saved,
            name=name,
            message=message,
            url=url,
            id=id,
            success=success,
            role=role,
        )

        edit_user_role_response.additional_properties = d
        return edit_user_role_response

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
