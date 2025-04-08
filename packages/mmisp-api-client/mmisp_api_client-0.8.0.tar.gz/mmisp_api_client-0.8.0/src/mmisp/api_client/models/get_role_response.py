from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.role_attribute_response import RoleAttributeResponse


T = TypeVar("T", bound="GetRoleResponse")


@_attrs_define
class GetRoleResponse:
    """
    Attributes:
        role (Union[Unset, RoleAttributeResponse]):
    """

    role: Union[Unset, "RoleAttributeResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["Role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_attribute_response import RoleAttributeResponse

        d = dict(src_dict)
        _role = d.pop("Role", UNSET)
        role: Union[Unset, RoleAttributeResponse]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = RoleAttributeResponse.from_dict(_role)

        get_role_response = cls(
            role=role,
        )

        get_role_response.additional_properties = d
        return get_role_response

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
