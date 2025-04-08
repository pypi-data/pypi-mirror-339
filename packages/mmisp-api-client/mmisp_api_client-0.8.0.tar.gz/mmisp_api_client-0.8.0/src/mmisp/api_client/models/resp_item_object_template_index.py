from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.object_template import ObjectTemplate


T = TypeVar("T", bound="RespItemObjectTemplateIndex")


@_attrs_define
class RespItemObjectTemplateIndex:
    """
    Attributes:
        object_template (ObjectTemplate):
    """

    object_template: "ObjectTemplate"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_template = self.object_template.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ObjectTemplate": object_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_template import ObjectTemplate

        d = dict(src_dict)
        object_template = ObjectTemplate.from_dict(d.pop("ObjectTemplate"))

        resp_item_object_template_index = cls(
            object_template=object_template,
        )

        resp_item_object_template_index.additional_properties = d
        return resp_item_object_template_index

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
