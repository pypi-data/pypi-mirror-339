from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ViewUpdateSharingGroupLegacyResponseOrganisationInfo")


@_attrs_define
class ViewUpdateSharingGroupLegacyResponseOrganisationInfo:
    """
    Attributes:
        id (int):
        uuid (str):
        name (str):
        local (bool):
    """

    id: int
    uuid: str
    name: str
    local: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        name = self.name

        local = self.local

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "name": name,
                "local": local,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        name = d.pop("name")

        local = d.pop("local")

        view_update_sharing_group_legacy_response_organisation_info = cls(
            id=id,
            uuid=uuid,
            name=name,
            local=local,
        )

        view_update_sharing_group_legacy_response_organisation_info.additional_properties = d
        return view_update_sharing_group_legacy_response_organisation_info

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
