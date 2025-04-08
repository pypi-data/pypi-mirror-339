from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchAttributesEvent")


@_attrs_define
class SearchAttributesEvent:
    """
    Attributes:
        id (int):
        org_id (int):
        distribution (str):
        info (str):
        orgc_id (int):
        uuid (str):
        publish_timestamp (int):
    """

    id: int
    org_id: int
    distribution: str
    info: str
    orgc_id: int
    uuid: str
    publish_timestamp: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        distribution = self.distribution

        info = self.info

        orgc_id = self.orgc_id

        uuid = self.uuid

        publish_timestamp = self.publish_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "distribution": distribution,
                "info": info,
                "orgc_id": orgc_id,
                "uuid": uuid,
                "publish_timestamp": publish_timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        distribution = d.pop("distribution")

        info = d.pop("info")

        orgc_id = d.pop("orgc_id")

        uuid = d.pop("uuid")

        publish_timestamp = d.pop("publish_timestamp")

        search_attributes_event = cls(
            id=id,
            org_id=org_id,
            distribution=distribution,
            info=info,
            orgc_id=orgc_id,
            uuid=uuid,
            publish_timestamp=publish_timestamp,
        )

        search_attributes_event.additional_properties = d
        return search_attributes_event

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
