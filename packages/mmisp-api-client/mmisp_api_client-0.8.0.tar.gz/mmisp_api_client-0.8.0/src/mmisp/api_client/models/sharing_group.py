import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SharingGroup")


@_attrs_define
class SharingGroup:
    """
    Attributes:
        id (int):
        name (str):
        releasability (str):
        description (str):
        uuid (str):
        organisation_uuid (str):
        org_id (int):
        sync_user_id (int):
        active (bool):
        created (Union[datetime.datetime, str]):
        modified (Union[datetime.datetime, str]):
        local (bool):
        roaming (bool):
    """

    id: int
    name: str
    releasability: str
    description: str
    uuid: str
    organisation_uuid: str
    org_id: int
    sync_user_id: int
    active: bool
    created: Union[datetime.datetime, str]
    modified: Union[datetime.datetime, str]
    local: bool
    roaming: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        releasability = self.releasability

        description = self.description

        uuid = self.uuid

        organisation_uuid = self.organisation_uuid

        org_id = self.org_id

        sync_user_id = self.sync_user_id

        active = self.active

        created: str
        if isinstance(self.created, datetime.datetime):
            created = self.created.isoformat()
        else:
            created = self.created

        modified: str
        if isinstance(self.modified, datetime.datetime):
            modified = self.modified.isoformat()
        else:
            modified = self.modified

        local = self.local

        roaming = self.roaming

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "releasability": releasability,
                "description": description,
                "uuid": uuid,
                "organisation_uuid": organisation_uuid,
                "org_id": org_id,
                "sync_user_id": sync_user_id,
                "active": active,
                "created": created,
                "modified": modified,
                "local": local,
                "roaming": roaming,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        releasability = d.pop("releasability")

        description = d.pop("description")

        uuid = d.pop("uuid")

        organisation_uuid = d.pop("organisation_uuid")

        org_id = d.pop("org_id")

        sync_user_id = d.pop("sync_user_id")

        active = d.pop("active")

        def _parse_created(data: object) -> Union[datetime.datetime, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_type_0 = isoparse(data)

                return created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[datetime.datetime, str], data)

        created = _parse_created(d.pop("created"))

        def _parse_modified(data: object) -> Union[datetime.datetime, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_type_0 = isoparse(data)

                return modified_type_0
            except:  # noqa: E722
                pass
            return cast(Union[datetime.datetime, str], data)

        modified = _parse_modified(d.pop("modified"))

        local = d.pop("local")

        roaming = d.pop("roaming")

        sharing_group = cls(
            id=id,
            name=name,
            releasability=releasability,
            description=description,
            uuid=uuid,
            organisation_uuid=organisation_uuid,
            org_id=org_id,
            sync_user_id=sync_user_id,
            active=active,
            created=created,
            modified=modified,
            local=local,
            roaming=roaming,
        )

        sharing_group.additional_properties = d
        return sharing_group

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
