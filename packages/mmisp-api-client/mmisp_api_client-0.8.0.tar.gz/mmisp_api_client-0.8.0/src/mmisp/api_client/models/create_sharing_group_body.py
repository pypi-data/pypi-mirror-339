from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSharingGroupBody")


@_attrs_define
class CreateSharingGroupBody:
    """
    Attributes:
        name (str):
        releasability (str):
        uuid (Union[Unset, str]):
        description (Union[Unset, str]):
        organisation_uuid (Union[Unset, str]):
        active (Union[Unset, bool]):
        roaming (Union[Unset, bool]):
        local (Union[Unset, bool]):
    """

    name: str
    releasability: str
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    organisation_uuid: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    roaming: Union[Unset, bool] = UNSET
    local: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        releasability = self.releasability

        uuid = self.uuid

        description = self.description

        organisation_uuid = self.organisation_uuid

        active = self.active

        roaming = self.roaming

        local = self.local

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "releasability": releasability,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if organisation_uuid is not UNSET:
            field_dict["organisation_uuid"] = organisation_uuid
        if active is not UNSET:
            field_dict["active"] = active
        if roaming is not UNSET:
            field_dict["roaming"] = roaming
        if local is not UNSET:
            field_dict["local"] = local

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        releasability = d.pop("releasability")

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        organisation_uuid = d.pop("organisation_uuid", UNSET)

        active = d.pop("active", UNSET)

        roaming = d.pop("roaming", UNSET)

        local = d.pop("local", UNSET)

        create_sharing_group_body = cls(
            name=name,
            releasability=releasability,
            uuid=uuid,
            description=description,
            organisation_uuid=organisation_uuid,
            active=active,
            roaming=roaming,
            local=local,
        )

        create_sharing_group_body.additional_properties = d
        return create_sharing_group_body

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
