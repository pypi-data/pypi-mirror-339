from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddAttributeViaFreeTextImportEventBody")


@_attrs_define
class AddAttributeViaFreeTextImportEventBody:
    """
    Attributes:
        value (str):
        return_meta_attributes (bool):
    """

    value: str
    return_meta_attributes: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        return_meta_attributes = self.return_meta_attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "returnMetaAttributes": return_meta_attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        return_meta_attributes = d.pop("returnMetaAttributes")

        add_attribute_via_free_text_import_event_body = cls(
            value=value,
            return_meta_attributes=return_meta_attributes,
        )

        add_attribute_via_free_text_import_event_body.additional_properties = d
        return add_attribute_via_free_text_import_event_body

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
