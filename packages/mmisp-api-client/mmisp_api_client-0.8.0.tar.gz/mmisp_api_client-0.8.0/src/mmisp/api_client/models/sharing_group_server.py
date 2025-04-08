from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SharingGroupServer")


@_attrs_define
class SharingGroupServer:
    """
    Attributes:
        id (int):
        sharing_group_id (int):
        server_id (int):
        all_orgs (bool):
    """

    id: int
    sharing_group_id: int
    server_id: int
    all_orgs: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sharing_group_id = self.sharing_group_id

        server_id = self.server_id

        all_orgs = self.all_orgs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sharing_group_id": sharing_group_id,
                "server_id": server_id,
                "all_orgs": all_orgs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        sharing_group_id = d.pop("sharing_group_id")

        server_id = d.pop("server_id")

        all_orgs = d.pop("all_orgs")

        sharing_group_server = cls(
            id=id,
            sharing_group_id=sharing_group_id,
            server_id=server_id,
            all_orgs=all_orgs,
        )

        sharing_group_server.additional_properties = d
        return sharing_group_server

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
