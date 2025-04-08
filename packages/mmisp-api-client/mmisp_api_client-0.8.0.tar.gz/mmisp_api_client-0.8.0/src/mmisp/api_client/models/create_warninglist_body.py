from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_warninglist_body_valid_attributes_item import CreateWarninglistBodyValidAttributesItem
from ..models.warninglist_category import WarninglistCategory
from ..models.warninglist_list_type import WarninglistListType

T = TypeVar("T", bound="CreateWarninglistBody")


@_attrs_define
class CreateWarninglistBody:
    """
    Attributes:
        name (str):
        type_ (WarninglistListType): An enumeration.
        description (str):
        enabled (bool):
        default (bool):
        category (WarninglistCategory): An enumeration.
        valid_attributes (list[CreateWarninglistBodyValidAttributesItem]):
        values (str):
    """

    name: str
    type_: WarninglistListType
    description: str
    enabled: bool
    default: bool
    category: WarninglistCategory
    valid_attributes: list[CreateWarninglistBodyValidAttributesItem]
    values: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        description = self.description

        enabled = self.enabled

        default = self.default

        category = self.category.value

        valid_attributes = []
        for valid_attributes_item_data in self.valid_attributes:
            valid_attributes_item = valid_attributes_item_data.value
            valid_attributes.append(valid_attributes_item)

        values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "description": description,
                "enabled": enabled,
                "default": default,
                "category": category,
                "valid_attributes": valid_attributes,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = WarninglistListType(d.pop("type"))

        description = d.pop("description")

        enabled = d.pop("enabled")

        default = d.pop("default")

        category = WarninglistCategory(d.pop("category"))

        valid_attributes = []
        _valid_attributes = d.pop("valid_attributes")
        for valid_attributes_item_data in _valid_attributes:
            valid_attributes_item = CreateWarninglistBodyValidAttributesItem(valid_attributes_item_data)

            valid_attributes.append(valid_attributes_item)

        values = d.pop("values")

        create_warninglist_body = cls(
            name=name,
            type_=type_,
            description=description,
            enabled=enabled,
            default=default,
            category=category,
            valid_attributes=valid_attributes,
            values=values,
        )

        create_warninglist_body.additional_properties = d
        return create_warninglist_body

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
