from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.object_template import ObjectTemplate
    from ..models.object_template_element import ObjectTemplateElement


T = TypeVar("T", bound="RespObjectTemplateView")


@_attrs_define
class RespObjectTemplateView:
    """
    Attributes:
        object_template (ObjectTemplate):
        object_template_element (list['ObjectTemplateElement']):
    """

    object_template: "ObjectTemplate"
    object_template_element: list["ObjectTemplateElement"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_template = self.object_template.to_dict()

        object_template_element = []
        for object_template_element_item_data in self.object_template_element:
            object_template_element_item = object_template_element_item_data.to_dict()
            object_template_element.append(object_template_element_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ObjectTemplate": object_template,
                "ObjectTemplateElement": object_template_element,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_template import ObjectTemplate
        from ..models.object_template_element import ObjectTemplateElement

        d = dict(src_dict)
        object_template = ObjectTemplate.from_dict(d.pop("ObjectTemplate"))

        object_template_element = []
        _object_template_element = d.pop("ObjectTemplateElement")
        for object_template_element_item_data in _object_template_element:
            object_template_element_item = ObjectTemplateElement.from_dict(object_template_element_item_data)

            object_template_element.append(object_template_element_item)

        resp_object_template_view = cls(
            object_template=object_template,
            object_template_element=object_template_element,
        )

        resp_object_template_view.additional_properties = d
        return resp_object_template_view

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
