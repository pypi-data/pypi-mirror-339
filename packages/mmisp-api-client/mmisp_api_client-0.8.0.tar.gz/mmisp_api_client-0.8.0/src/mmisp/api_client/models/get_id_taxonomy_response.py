from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.taxonomy_entry_schema import TaxonomyEntrySchema


T = TypeVar("T", bound="GetIdTaxonomyResponse")


@_attrs_define
class GetIdTaxonomyResponse:
    """
    Attributes:
        id (int):
        namespace (str):
        description (str):
        version (str):
        enabled (bool):
        exclusive (bool):
        required (bool):
        highlighted (bool):
        entries (list['TaxonomyEntrySchema']):
    """

    id: int
    namespace: str
    description: str
    version: str
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool
    entries: list["TaxonomyEntrySchema"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        namespace = self.namespace

        description = self.description

        version = self.version

        enabled = self.enabled

        exclusive = self.exclusive

        required = self.required

        highlighted = self.highlighted

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "namespace": namespace,
                "description": description,
                "version": version,
                "enabled": enabled,
                "exclusive": exclusive,
                "required": required,
                "highlighted": highlighted,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.taxonomy_entry_schema import TaxonomyEntrySchema

        d = dict(src_dict)
        id = d.pop("id")

        namespace = d.pop("namespace")

        description = d.pop("description")

        version = d.pop("version")

        enabled = d.pop("enabled")

        exclusive = d.pop("exclusive")

        required = d.pop("required")

        highlighted = d.pop("highlighted")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = TaxonomyEntrySchema.from_dict(entries_item_data)

            entries.append(entries_item)

        get_id_taxonomy_response = cls(
            id=id,
            namespace=namespace,
            description=description,
            version=version,
            enabled=enabled,
            exclusive=exclusive,
            required=required,
            highlighted=highlighted,
            entries=entries,
        )

        get_id_taxonomy_response.additional_properties = d
        return get_id_taxonomy_response

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
