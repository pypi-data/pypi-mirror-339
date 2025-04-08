from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WarninglistAttributes")


@_attrs_define
class WarninglistAttributes:
    """
    Attributes:
        id (int):
        name (str):
        type_ (str):
        description (str):
        version (str):
        enabled (bool):
        default (bool):
        category (str):
        warninglist_entry_count (str):
        valid_attributes (str):
    """

    id: int
    name: str
    type_: str
    description: str
    version: str
    enabled: bool
    default: bool
    category: str
    warninglist_entry_count: str
    valid_attributes: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        type_ = self.type_

        description = self.description

        version = self.version

        enabled = self.enabled

        default = self.default

        category = self.category

        warninglist_entry_count = self.warninglist_entry_count

        valid_attributes = self.valid_attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "description": description,
                "version": version,
                "enabled": enabled,
                "default": default,
                "category": category,
                "warninglist_entry_count": warninglist_entry_count,
                "valid_attributes": valid_attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        type_ = d.pop("type")

        description = d.pop("description")

        version = d.pop("version")

        enabled = d.pop("enabled")

        default = d.pop("default")

        category = d.pop("category")

        warninglist_entry_count = d.pop("warninglist_entry_count")

        valid_attributes = d.pop("valid_attributes")

        warninglist_attributes = cls(
            id=id,
            name=name,
            type_=type_,
            description=description,
            version=version,
            enabled=enabled,
            default=default,
            category=category,
            warninglist_entry_count=warninglist_entry_count,
            valid_attributes=valid_attributes,
        )

        warninglist_attributes.additional_properties = d
        return warninglist_attributes

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
