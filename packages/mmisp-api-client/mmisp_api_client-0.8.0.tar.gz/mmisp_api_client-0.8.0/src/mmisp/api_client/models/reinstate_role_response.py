from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.role_attribute_response import RoleAttributeResponse


T = TypeVar("T", bound="ReinstateRoleResponse")


@_attrs_define
class ReinstateRoleResponse:
    """
    Attributes:
        role (RoleAttributeResponse):
        success (bool):
        message (str):
        url (str):
        id (int):
    """

    role: "RoleAttributeResponse"
    success: bool
    message: str
    url: str
    id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.to_dict()

        success = self.success

        message = self.message

        url = self.url

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Role": role,
                "success": success,
                "message": message,
                "url": url,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_attribute_response import RoleAttributeResponse

        d = dict(src_dict)
        role = RoleAttributeResponse.from_dict(d.pop("Role"))

        success = d.pop("success")

        message = d.pop("message")

        url = d.pop("url")

        id = d.pop("id")

        reinstate_role_response = cls(
            role=role,
            success=success,
            message=message,
            url=url,
            id=id,
        )

        reinstate_role_response.additional_properties = d
        return reinstate_role_response

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
