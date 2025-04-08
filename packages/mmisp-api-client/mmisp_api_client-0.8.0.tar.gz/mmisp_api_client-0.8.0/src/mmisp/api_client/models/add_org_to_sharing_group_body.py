from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddOrgToSharingGroupBody")


@_attrs_define
class AddOrgToSharingGroupBody:
    """
    Attributes:
        organisation_id (int):
        extend (Union[Unset, bool]):
    """

    organisation_id: int
    extend: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organisation_id = self.organisation_id

        extend = self.extend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organisationId": organisation_id,
            }
        )
        if extend is not UNSET:
            field_dict["extend"] = extend

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organisation_id = d.pop("organisationId")

        extend = d.pop("extend", UNSET)

        add_org_to_sharing_group_body = cls(
            organisation_id=organisation_id,
            extend=extend,
        )

        add_org_to_sharing_group_body.additional_properties = d
        return add_org_to_sharing_group_body

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
