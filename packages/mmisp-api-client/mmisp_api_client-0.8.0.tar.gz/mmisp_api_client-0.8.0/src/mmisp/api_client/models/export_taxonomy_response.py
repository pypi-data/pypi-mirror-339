from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.taxonomy_predicate_schema import TaxonomyPredicateSchema
    from ..models.taxonomy_value_schema import TaxonomyValueSchema


T = TypeVar("T", bound="ExportTaxonomyResponse")


@_attrs_define
class ExportTaxonomyResponse:
    """
    Attributes:
        namespace (str):
        description (str):
        version (int):
        exclusive (bool):
        predicates (list['TaxonomyPredicateSchema']):
        values (list['TaxonomyValueSchema']):
    """

    namespace: str
    description: str
    version: int
    exclusive: bool
    predicates: list["TaxonomyPredicateSchema"]
    values: list["TaxonomyValueSchema"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        namespace = self.namespace

        description = self.description

        version = self.version

        exclusive = self.exclusive

        predicates = []
        for predicates_item_data in self.predicates:
            predicates_item = predicates_item_data.to_dict()
            predicates.append(predicates_item)

        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "namespace": namespace,
                "description": description,
                "version": version,
                "exclusive": exclusive,
                "predicates": predicates,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.taxonomy_predicate_schema import TaxonomyPredicateSchema
        from ..models.taxonomy_value_schema import TaxonomyValueSchema

        d = dict(src_dict)
        namespace = d.pop("namespace")

        description = d.pop("description")

        version = d.pop("version")

        exclusive = d.pop("exclusive")

        predicates = []
        _predicates = d.pop("predicates")
        for predicates_item_data in _predicates:
            predicates_item = TaxonomyPredicateSchema.from_dict(predicates_item_data)

            predicates.append(predicates_item)

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = TaxonomyValueSchema.from_dict(values_item_data)

            values.append(values_item)

        export_taxonomy_response = cls(
            namespace=namespace,
            description=description,
            version=version,
            exclusive=exclusive,
            predicates=predicates,
            values=values,
        )

        export_taxonomy_response.additional_properties = d
        return export_taxonomy_response

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
