from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_tag_attributes_response import PartialTagAttributesResponse
    from ..models.partial_taxonomy_predicate_response import PartialTaxonomyPredicateResponse
    from ..models.partial_taxonomy_view import PartialTaxonomyView


T = TypeVar("T", bound="PartialTagCombinedModel")


@_attrs_define
class PartialTagCombinedModel:
    """
    Attributes:
        tag (Union[Unset, PartialTagAttributesResponse]):
        taxonomy (Union[Unset, PartialTaxonomyView]):
        taxonomy_predicate (Union[Unset, PartialTaxonomyPredicateResponse]):
    """

    tag: Union[Unset, "PartialTagAttributesResponse"] = UNSET
    taxonomy: Union[Unset, "PartialTaxonomyView"] = UNSET
    taxonomy_predicate: Union[Unset, "PartialTaxonomyPredicateResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tag: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.to_dict()

        taxonomy: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.taxonomy, Unset):
            taxonomy = self.taxonomy.to_dict()

        taxonomy_predicate: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.taxonomy_predicate, Unset):
            taxonomy_predicate = self.taxonomy_predicate.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tag is not UNSET:
            field_dict["Tag"] = tag
        if taxonomy is not UNSET:
            field_dict["Taxonomy"] = taxonomy
        if taxonomy_predicate is not UNSET:
            field_dict["TaxonomyPredicate"] = taxonomy_predicate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partial_tag_attributes_response import PartialTagAttributesResponse
        from ..models.partial_taxonomy_predicate_response import PartialTaxonomyPredicateResponse
        from ..models.partial_taxonomy_view import PartialTaxonomyView

        d = dict(src_dict)
        _tag = d.pop("Tag", UNSET)
        tag: Union[Unset, PartialTagAttributesResponse]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = PartialTagAttributesResponse.from_dict(_tag)

        _taxonomy = d.pop("Taxonomy", UNSET)
        taxonomy: Union[Unset, PartialTaxonomyView]
        if isinstance(_taxonomy, Unset):
            taxonomy = UNSET
        else:
            taxonomy = PartialTaxonomyView.from_dict(_taxonomy)

        _taxonomy_predicate = d.pop("TaxonomyPredicate", UNSET)
        taxonomy_predicate: Union[Unset, PartialTaxonomyPredicateResponse]
        if isinstance(_taxonomy_predicate, Unset):
            taxonomy_predicate = UNSET
        else:
            taxonomy_predicate = PartialTaxonomyPredicateResponse.from_dict(_taxonomy_predicate)

        partial_tag_combined_model = cls(
            tag=tag,
            taxonomy=taxonomy,
            taxonomy_predicate=taxonomy_predicate,
        )

        partial_tag_combined_model.additional_properties = d
        return partial_tag_combined_model

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
