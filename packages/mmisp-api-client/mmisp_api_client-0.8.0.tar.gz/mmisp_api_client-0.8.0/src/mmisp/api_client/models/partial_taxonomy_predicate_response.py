from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialTaxonomyPredicateResponse")


@_attrs_define
class PartialTaxonomyPredicateResponse:
    """
    Attributes:
        value (Union[Unset, str]):
        expanded (Union[Unset, str]):
        description (Union[Unset, str]):
        id (Union[Unset, int]):
        taxonomy_id (Union[Unset, int]):
        colour (Union[Unset, str]):
        exclusive (Union[Unset, bool]):
        numerical_value (Union[Unset, int]):
    """

    value: Union[Unset, str] = UNSET
    expanded: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    id: Union[Unset, int] = UNSET
    taxonomy_id: Union[Unset, int] = UNSET
    colour: Union[Unset, str] = UNSET
    exclusive: Union[Unset, bool] = UNSET
    numerical_value: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        expanded = self.expanded

        description = self.description

        id = self.id

        taxonomy_id = self.taxonomy_id

        colour = self.colour

        exclusive = self.exclusive

        numerical_value = self.numerical_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if expanded is not UNSET:
            field_dict["expanded"] = expanded
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if taxonomy_id is not UNSET:
            field_dict["taxonomy_id"] = taxonomy_id
        if colour is not UNSET:
            field_dict["colour"] = colour
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if numerical_value is not UNSET:
            field_dict["numerical_value"] = numerical_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value", UNSET)

        expanded = d.pop("expanded", UNSET)

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        taxonomy_id = d.pop("taxonomy_id", UNSET)

        colour = d.pop("colour", UNSET)

        exclusive = d.pop("exclusive", UNSET)

        numerical_value = d.pop("numerical_value", UNSET)

        partial_taxonomy_predicate_response = cls(
            value=value,
            expanded=expanded,
            description=description,
            id=id,
            taxonomy_id=taxonomy_id,
            colour=colour,
            exclusive=exclusive,
            numerical_value=numerical_value,
        )

        partial_taxonomy_predicate_response.additional_properties = d
        return partial_taxonomy_predicate_response

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
