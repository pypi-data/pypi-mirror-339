from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_describe_types_attributes_category_type_mappings import (
        GetDescribeTypesAttributesCategoryTypeMappings,
    )
    from ..models.get_describe_types_attributes_sane_defaults import GetDescribeTypesAttributesSaneDefaults


T = TypeVar("T", bound="GetDescribeTypesAttributes")


@_attrs_define
class GetDescribeTypesAttributes:
    """
    Attributes:
        sane_defaults (Union[Unset, GetDescribeTypesAttributesSaneDefaults]):
        types (Union[Unset, list[str]]):
        categories (Union[Unset, list[str]]):
        category_type_mappings (Union[Unset, GetDescribeTypesAttributesCategoryTypeMappings]):
    """

    sane_defaults: Union[Unset, "GetDescribeTypesAttributesSaneDefaults"] = UNSET
    types: Union[Unset, list[str]] = UNSET
    categories: Union[Unset, list[str]] = UNSET
    category_type_mappings: Union[Unset, "GetDescribeTypesAttributesCategoryTypeMappings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sane_defaults: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sane_defaults, Unset):
            sane_defaults = self.sane_defaults.to_dict()

        types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = self.types

        categories: Union[Unset, list[str]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = self.categories

        category_type_mappings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.category_type_mappings, Unset):
            category_type_mappings = self.category_type_mappings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sane_defaults is not UNSET:
            field_dict["sane_defaults"] = sane_defaults
        if types is not UNSET:
            field_dict["types"] = types
        if categories is not UNSET:
            field_dict["categories"] = categories
        if category_type_mappings is not UNSET:
            field_dict["category_type_mappings"] = category_type_mappings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_describe_types_attributes_category_type_mappings import (
            GetDescribeTypesAttributesCategoryTypeMappings,
        )
        from ..models.get_describe_types_attributes_sane_defaults import GetDescribeTypesAttributesSaneDefaults

        d = dict(src_dict)
        _sane_defaults = d.pop("sane_defaults", UNSET)
        sane_defaults: Union[Unset, GetDescribeTypesAttributesSaneDefaults]
        if isinstance(_sane_defaults, Unset):
            sane_defaults = UNSET
        else:
            sane_defaults = GetDescribeTypesAttributesSaneDefaults.from_dict(_sane_defaults)

        types = cast(list[str], d.pop("types", UNSET))

        categories = cast(list[str], d.pop("categories", UNSET))

        _category_type_mappings = d.pop("category_type_mappings", UNSET)
        category_type_mappings: Union[Unset, GetDescribeTypesAttributesCategoryTypeMappings]
        if isinstance(_category_type_mappings, Unset):
            category_type_mappings = UNSET
        else:
            category_type_mappings = GetDescribeTypesAttributesCategoryTypeMappings.from_dict(_category_type_mappings)

        get_describe_types_attributes = cls(
            sane_defaults=sane_defaults,
            types=types,
            categories=categories,
            category_type_mappings=category_type_mappings,
        )

        get_describe_types_attributes.additional_properties = d
        return get_describe_types_attributes

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
