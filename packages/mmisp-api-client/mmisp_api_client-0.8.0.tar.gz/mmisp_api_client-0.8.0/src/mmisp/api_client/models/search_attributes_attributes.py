from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.search_attributes_attributes_details import SearchAttributesAttributesDetails


T = TypeVar("T", bound="SearchAttributesAttributes")


@_attrs_define
class SearchAttributesAttributes:
    """
    Attributes:
        attribute (list['SearchAttributesAttributesDetails']):
    """

    attribute: list["SearchAttributesAttributesDetails"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute = []
        for attribute_item_data in self.attribute:
            attribute_item = attribute_item_data.to_dict()
            attribute.append(attribute_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Attribute": attribute,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_attributes_attributes_details import SearchAttributesAttributesDetails

        d = dict(src_dict)
        attribute = []
        _attribute = d.pop("Attribute")
        for attribute_item_data in _attribute:
            attribute_item = SearchAttributesAttributesDetails.from_dict(attribute_item_data)

            attribute.append(attribute_item)

        search_attributes_attributes = cls(
            attribute=attribute,
        )

        search_attributes_attributes.additional_properties = d
        return search_attributes_attributes

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
