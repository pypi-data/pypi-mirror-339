from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddServerToSharingGroupBody")


@_attrs_define
class AddServerToSharingGroupBody:
    """
    Attributes:
        server_id (int):
        all_orgs (Union[Unset, bool]):
    """

    server_id: int
    all_orgs: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        server_id = self.server_id

        all_orgs = self.all_orgs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serverId": server_id,
            }
        )
        if all_orgs is not UNSET:
            field_dict["all_orgs"] = all_orgs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_id = d.pop("serverId")

        all_orgs = d.pop("all_orgs", UNSET)

        add_server_to_sharing_group_body = cls(
            server_id=server_id,
            all_orgs=all_orgs,
        )

        add_server_to_sharing_group_body.additional_properties = d
        return add_server_to_sharing_group_body

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
