from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar(
    "T",
    bound="RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete",
)


@_attrs_define
class RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete:
    """ """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        remove_server_from_sharing_group_sharing_groups_id_servers_server_id_delete_response_remove_server_from_sharing_group_sharing_groups_id_servers_serverid_delete = cls()

        remove_server_from_sharing_group_sharing_groups_id_servers_server_id_delete_response_remove_server_from_sharing_group_sharing_groups_id_servers_serverid_delete.additional_properties = d
        return remove_server_from_sharing_group_sharing_groups_id_servers_server_id_delete_response_remove_server_from_sharing_group_sharing_groups_id_servers_serverid_delete

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
