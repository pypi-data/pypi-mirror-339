from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.taxonomy_view import TaxonomyView


T = TypeVar("T", bound="ViewTaxonomyResponse")


@_attrs_define
class ViewTaxonomyResponse:
    """
    Attributes:
        taxonomy (TaxonomyView):
        total_count (int):
        current_count (int):
    """

    taxonomy: "TaxonomyView"
    total_count: int
    current_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        taxonomy = self.taxonomy.to_dict()

        total_count = self.total_count

        current_count = self.current_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Taxonomy": taxonomy,
                "total_count": total_count,
                "current_count": current_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.taxonomy_view import TaxonomyView

        d = dict(src_dict)
        taxonomy = TaxonomyView.from_dict(d.pop("Taxonomy"))

        total_count = d.pop("total_count")

        current_count = d.pop("current_count")

        view_taxonomy_response = cls(
            taxonomy=taxonomy,
            total_count=total_count,
            current_count=current_count,
        )

        view_taxonomy_response.additional_properties = d
        return view_taxonomy_response

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
