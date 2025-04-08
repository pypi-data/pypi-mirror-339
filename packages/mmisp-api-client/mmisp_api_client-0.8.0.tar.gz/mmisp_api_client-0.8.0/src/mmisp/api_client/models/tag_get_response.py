from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.tag_attributes_response import TagAttributesResponse


T = TypeVar("T", bound="TagGetResponse")


@_attrs_define
class TagGetResponse:
    """
    Attributes:
        tag (list['TagAttributesResponse']):
    """

    tag: list["TagAttributesResponse"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tag = []
        for tag_item_data in self.tag:
            tag_item = tag_item_data.to_dict()
            tag.append(tag_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Tag": tag,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tag_attributes_response import TagAttributesResponse

        d = dict(src_dict)
        tag = []
        _tag = d.pop("Tag")
        for tag_item_data in _tag:
            tag_item = TagAttributesResponse.from_dict(tag_item_data)

            tag.append(tag_item)

        tag_get_response = cls(
            tag=tag,
        )

        tag_get_response.additional_properties = d
        return tag_get_response

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
