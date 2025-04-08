from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddEditGetEventShadowAttribute")


@_attrs_define
class AddEditGetEventShadowAttribute:
    """
    Attributes:
        value (str):
        to_ids (bool):
        type_ (str):
        category (str):
    """

    value: str
    to_ids: bool
    type_: str
    category: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        to_ids = self.to_ids

        type_ = self.type_

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "to_ids": to_ids,
                "type": type_,
                "category": category,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        to_ids = d.pop("to_ids")

        type_ = d.pop("type")

        category = d.pop("category")

        add_edit_get_event_shadow_attribute = cls(
            value=value,
            to_ids=to_ids,
            type_=type_,
            category=category,
        )

        add_edit_get_event_shadow_attribute.additional_properties = d
        return add_edit_get_event_shadow_attribute

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
