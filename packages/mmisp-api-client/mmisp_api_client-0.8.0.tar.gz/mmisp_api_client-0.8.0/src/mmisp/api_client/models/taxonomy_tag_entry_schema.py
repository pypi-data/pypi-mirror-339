from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.tag_attributes_response import TagAttributesResponse


T = TypeVar("T", bound="TaxonomyTagEntrySchema")


@_attrs_define
class TaxonomyTagEntrySchema:
    """
    Attributes:
        tag (str):
        expanded (str):
        exclusive_predicate (bool):
        description (str):
        existing_tag (Union['TagAttributesResponse', bool]):
        events (int):
        attributes (int):
    """

    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: Union["TagAttributesResponse", bool]
    events: int
    attributes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.tag_attributes_response import TagAttributesResponse

        tag = self.tag

        expanded = self.expanded

        exclusive_predicate = self.exclusive_predicate

        description = self.description

        existing_tag: Union[bool, dict[str, Any]]
        if isinstance(self.existing_tag, TagAttributesResponse):
            existing_tag = self.existing_tag.to_dict()
        else:
            existing_tag = self.existing_tag

        events = self.events

        attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tag": tag,
                "expanded": expanded,
                "exclusive_predicate": exclusive_predicate,
                "description": description,
                "existing_tag": existing_tag,
                "events": events,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tag_attributes_response import TagAttributesResponse

        d = dict(src_dict)
        tag = d.pop("tag")

        expanded = d.pop("expanded")

        exclusive_predicate = d.pop("exclusive_predicate")

        description = d.pop("description")

        def _parse_existing_tag(data: object) -> Union["TagAttributesResponse", bool]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                existing_tag_type_1 = TagAttributesResponse.from_dict(data)

                return existing_tag_type_1
            except:  # noqa: E722
                pass
            return cast(Union["TagAttributesResponse", bool], data)

        existing_tag = _parse_existing_tag(d.pop("existing_tag"))

        events = d.pop("events")

        attributes = d.pop("attributes")

        taxonomy_tag_entry_schema = cls(
            tag=tag,
            expanded=expanded,
            exclusive_predicate=exclusive_predicate,
            description=description,
            existing_tag=existing_tag,
            events=events,
            attributes=attributes,
        )

        taxonomy_tag_entry_schema.additional_properties = d
        return taxonomy_tag_entry_schema

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
