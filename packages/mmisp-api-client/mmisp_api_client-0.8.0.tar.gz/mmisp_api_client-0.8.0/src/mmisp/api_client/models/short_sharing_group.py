from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShortSharingGroup")


@_attrs_define
class ShortSharingGroup:
    """
    Attributes:
        id (int):
        name (str):
        releasability (str):
        description (str):
        uuid (str):
        active (bool):
        local (bool):
        roaming (bool):
        org_count (Union[Unset, int]):  Default: 0.
    """

    id: int
    name: str
    releasability: str
    description: str
    uuid: str
    active: bool
    local: bool
    roaming: bool
    org_count: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        releasability = self.releasability

        description = self.description

        uuid = self.uuid

        active = self.active

        local = self.local

        roaming = self.roaming

        org_count = self.org_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "releasability": releasability,
                "description": description,
                "uuid": uuid,
                "active": active,
                "local": local,
                "roaming": roaming,
            }
        )
        if org_count is not UNSET:
            field_dict["org_count"] = org_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        releasability = d.pop("releasability")

        description = d.pop("description")

        uuid = d.pop("uuid")

        active = d.pop("active")

        local = d.pop("local")

        roaming = d.pop("roaming")

        org_count = d.pop("org_count", UNSET)

        short_sharing_group = cls(
            id=id,
            name=name,
            releasability=releasability,
            description=description,
            uuid=uuid,
            active=active,
            local=local,
            roaming=roaming,
            org_count=org_count,
        )

        short_sharing_group.additional_properties = d
        return short_sharing_group

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
