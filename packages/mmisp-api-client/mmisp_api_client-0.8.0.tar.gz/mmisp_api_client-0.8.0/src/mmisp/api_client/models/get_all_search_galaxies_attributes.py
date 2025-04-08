import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.distribution_levels import DistributionLevels
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAllSearchGalaxiesAttributes")


@_attrs_define
class GetAllSearchGalaxiesAttributes:
    """
    Attributes:
        id (int):
        uuid (str):
        name (str):
        type_ (str):
        description (str):
        version (str):
        icon (str):
        namespace (str):
        enabled (bool):
        local_only (bool):
        created (Union[datetime.datetime, str]):
        modified (Union[datetime.datetime, str]):
        org_id (int):
        orgc_id (int):
        default (bool):
        distribution (DistributionLevels): An enumeration.
        kill_chain_order (Union[Unset, str]):
    """

    id: int
    uuid: str
    name: str
    type_: str
    description: str
    version: str
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    created: Union[datetime.datetime, str]
    modified: Union[datetime.datetime, str]
    org_id: int
    orgc_id: int
    default: bool
    distribution: DistributionLevels
    kill_chain_order: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        name = self.name

        type_ = self.type_

        description = self.description

        version = self.version

        icon = self.icon

        namespace = self.namespace

        enabled = self.enabled

        local_only = self.local_only

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

        org_id = self.org_id

        orgc_id = self.orgc_id

        default = self.default

        distribution = self.distribution.value

        kill_chain_order = self.kill_chain_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "name": name,
                "type": type_,
                "description": description,
                "version": version,
                "icon": icon,
                "namespace": namespace,
                "enabled": enabled,
                "local_only": local_only,
                "created": created,
                "modified": modified,
                "org_id": org_id,
                "orgc_id": orgc_id,
                "default": default,
                "distribution": distribution,
            }
        )
        if kill_chain_order is not UNSET:
            field_dict["kill_chain_order"] = kill_chain_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        name = d.pop("name")

        type_ = d.pop("type")

        description = d.pop("description")

        version = d.pop("version")

        icon = d.pop("icon")

        namespace = d.pop("namespace")

        enabled = d.pop("enabled")

        local_only = d.pop("local_only")

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

        org_id = d.pop("org_id")

        orgc_id = d.pop("orgc_id")

        default = d.pop("default")

        distribution = DistributionLevels(d.pop("distribution"))

        kill_chain_order = d.pop("kill_chain_order", UNSET)

        get_all_search_galaxies_attributes = cls(
            id=id,
            uuid=uuid,
            name=name,
            type_=type_,
            description=description,
            version=version,
            icon=icon,
            namespace=namespace,
            enabled=enabled,
            local_only=local_only,
            created=created,
            modified=modified,
            org_id=org_id,
            orgc_id=orgc_id,
            default=default,
            distribution=distribution,
            kill_chain_order=kill_chain_order,
        )

        get_all_search_galaxies_attributes.additional_properties = d
        return get_all_search_galaxies_attributes

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
