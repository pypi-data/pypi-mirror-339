from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.add_edit_get_event_related_event_attributes import AddEditGetEventRelatedEventAttributes


T = TypeVar("T", bound="AddEditGetEventRelatedEvent")


@_attrs_define
class AddEditGetEventRelatedEvent:
    """
    Attributes:
        event (AddEditGetEventRelatedEventAttributes):
        relationship_inbound (list[Any]):
    """

    event: "AddEditGetEventRelatedEventAttributes"
    relationship_inbound: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event = self.event.to_dict()

        relationship_inbound = self.relationship_inbound

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Event": event,
                "RelationshipInbound": relationship_inbound,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_related_event_attributes import AddEditGetEventRelatedEventAttributes

        d = dict(src_dict)
        event = AddEditGetEventRelatedEventAttributes.from_dict(d.pop("Event"))

        relationship_inbound = cast(list[Any], d.pop("RelationshipInbound"))

        add_edit_get_event_related_event = cls(
            event=event,
            relationship_inbound=relationship_inbound,
        )

        add_edit_get_event_related_event.additional_properties = d
        return add_edit_get_event_related_event

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
