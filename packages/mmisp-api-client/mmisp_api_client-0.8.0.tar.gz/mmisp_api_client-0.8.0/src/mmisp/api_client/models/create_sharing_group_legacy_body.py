import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateSharingGroupLegacyBody")


@_attrs_define
class CreateSharingGroupLegacyBody:
    """
    Attributes:
        name (str):
        uuid (Union[Unset, str]):
        description (Union[Unset, str]):
        releasability (Union[Unset, str]):
        local (Union[Unset, bool]):
        active (Union[Unset, bool]):
        org_count (Union[Unset, str]):
        organisation_uuid (Union[Unset, str]):
        org_id (Union[Unset, int]):
        sync_user_id (Union[Unset, int]):
        created (Union[Unset, datetime.datetime, str]):
        modified (Union[Unset, datetime.datetime, str]):
        roaming (Union[Unset, bool]):
    """

    name: str
    uuid: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    releasability: Union[Unset, str] = UNSET
    local: Union[Unset, bool] = UNSET
    active: Union[Unset, bool] = UNSET
    org_count: Union[Unset, str] = UNSET
    organisation_uuid: Union[Unset, str] = UNSET
    org_id: Union[Unset, int] = UNSET
    sync_user_id: Union[Unset, int] = UNSET
    created: Union[Unset, datetime.datetime, str] = UNSET
    modified: Union[Unset, datetime.datetime, str] = UNSET
    roaming: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = self.uuid

        description = self.description

        releasability = self.releasability

        local = self.local

        active = self.active

        org_count = self.org_count

        organisation_uuid = self.organisation_uuid

        org_id = self.org_id

        sync_user_id = self.sync_user_id

        created: Union[Unset, str]
        if isinstance(self.created, Unset):
            created = UNSET
        elif isinstance(self.created, datetime.datetime):
            created = self.created.isoformat()
        else:
            created = self.created

        modified: Union[Unset, str]
        if isinstance(self.modified, Unset):
            modified = UNSET
        elif isinstance(self.modified, datetime.datetime):
            modified = self.modified.isoformat()
        else:
            modified = self.modified

        roaming = self.roaming

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if releasability is not UNSET:
            field_dict["releasability"] = releasability
        if local is not UNSET:
            field_dict["local"] = local
        if active is not UNSET:
            field_dict["active"] = active
        if org_count is not UNSET:
            field_dict["org_count"] = org_count
        if organisation_uuid is not UNSET:
            field_dict["organisation_uuid"] = organisation_uuid
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if sync_user_id is not UNSET:
            field_dict["sync_user_id"] = sync_user_id
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if roaming is not UNSET:
            field_dict["roaming"] = roaming

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uuid = d.pop("uuid", UNSET)

        description = d.pop("description", UNSET)

        releasability = d.pop("releasability", UNSET)

        local = d.pop("local", UNSET)

        active = d.pop("active", UNSET)

        org_count = d.pop("org_count", UNSET)

        organisation_uuid = d.pop("organisation_uuid", UNSET)

        org_id = d.pop("org_id", UNSET)

        sync_user_id = d.pop("sync_user_id", UNSET)

        def _parse_created(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_type_0 = isoparse(data)

                return created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        created = _parse_created(d.pop("created", UNSET))

        def _parse_modified(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_type_0 = isoparse(data)

                return modified_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        modified = _parse_modified(d.pop("modified", UNSET))

        roaming = d.pop("roaming", UNSET)

        create_sharing_group_legacy_body = cls(
            name=name,
            uuid=uuid,
            description=description,
            releasability=releasability,
            local=local,
            active=active,
            org_count=org_count,
            organisation_uuid=organisation_uuid,
            org_id=org_id,
            sync_user_id=sync_user_id,
            created=created,
            modified=modified,
            roaming=roaming,
        )

        create_sharing_group_legacy_body.additional_properties = d
        return create_sharing_group_legacy_body

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
