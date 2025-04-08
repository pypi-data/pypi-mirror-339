from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.role_attribute_response import RoleAttributeResponse


T = TypeVar("T", bound="DefaultRoleResponse")


@_attrs_define
class DefaultRoleResponse:
    """
    Attributes:
        saved (bool):
        name (str):
        message (str):
        url (str):
        id (int):
        role (Union[Unset, RoleAttributeResponse]):
        success (Union[Unset, bool]):
        errors (Union[Unset, str]):
    """

    saved: bool
    name: str
    message: str
    url: str
    id: int
    role: Union[Unset, "RoleAttributeResponse"] = UNSET
    success: Union[Unset, bool] = UNSET
    errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        name = self.name

        message = self.message

        url = self.url

        id = self.id

        role: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.to_dict()

        success = self.success

        errors = self.errors

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
        if role is not UNSET:
            field_dict["Role"] = role
        if success is not UNSET:
            field_dict["success"] = success
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_attribute_response import RoleAttributeResponse

        d = dict(src_dict)
        saved = d.pop("saved")

        name = d.pop("name")

        message = d.pop("message")

        url = d.pop("url")

        id = d.pop("id")

        _role = d.pop("Role", UNSET)
        role: Union[Unset, RoleAttributeResponse]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RoleAttributeResponse.from_dict(_role)

        success = d.pop("success", UNSET)

        errors = d.pop("errors", UNSET)

        default_role_response = cls(
            saved=saved,
            name=name,
            message=message,
            url=url,
            id=id,
            role=role,
            success=success,
            errors=errors,
        )

        default_role_response.additional_properties = d
        return default_role_response

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
