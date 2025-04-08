from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddEditGetEventEventReport")


@_attrs_define
class AddEditGetEventEventReport:
    """
    Attributes:
        id (int):
        uuid (str):
        event_id (int):
        name (str):
        content (str):
        distribution (str):
        sharing_group_id (int):
        timestamp (str):
        deleted (bool):
    """

    id: int
    uuid: str
    event_id: int
    name: str
    content: str
    distribution: str
    sharing_group_id: int
    timestamp: str
    deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        event_id = self.event_id

        name = self.name

        content = self.content

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        timestamp = self.timestamp

        deleted = self.deleted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "event_id": event_id,
                "name": name,
                "content": content,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "timestamp": timestamp,
                "deleted": deleted,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        event_id = d.pop("event_id")

        name = d.pop("name")

        content = d.pop("content")

        distribution = d.pop("distribution")

        sharing_group_id = d.pop("sharing_group_id")

        timestamp = d.pop("timestamp")

        deleted = d.pop("deleted")

        add_edit_get_event_event_report = cls(
            id=id,
            uuid=uuid,
            event_id=event_id,
            name=name,
            content=content,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            timestamp=timestamp,
            deleted=deleted,
        )

        add_edit_get_event_event_report.additional_properties = d
        return add_edit_get_event_event_report

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
