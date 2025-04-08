from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectTemplateElement")


@_attrs_define
class ObjectTemplateElement:
    """
    Attributes:
        id (int):
        object_template_id (int):
        object_relation (str):
        type_ (str):
        ui_priority (int):
        categories (list[Any]):
        sane_default (list[Any]):
        values_list (list[Any]):
        description (str):
        multiple (bool):
        disable_correlation (Union[Unset, bool]):
    """

    id: int
    object_template_id: int
    object_relation: str
    type_: str
    ui_priority: int
    categories: list[Any]
    sane_default: list[Any]
    values_list: list[Any]
    description: str
    multiple: bool
    disable_correlation: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        object_template_id = self.object_template_id

        object_relation = self.object_relation

        type_ = self.type_

        ui_priority = self.ui_priority

        categories = self.categories

        sane_default = self.sane_default

        values_list = self.values_list

        description = self.description

        multiple = self.multiple

        disable_correlation = self.disable_correlation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object_template_id": object_template_id,
                "object_relation": object_relation,
                "type": type_,
                "ui-priority": ui_priority,
                "categories": categories,
                "sane_default": sane_default,
                "values_list": values_list,
                "description": description,
                "multiple": multiple,
            }
        )
        if disable_correlation is not UNSET:
            field_dict["disable_correlation"] = disable_correlation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        object_template_id = d.pop("object_template_id")

        object_relation = d.pop("object_relation")

        type_ = d.pop("type")

        ui_priority = d.pop("ui-priority")

        categories = cast(list[Any], d.pop("categories"))

        sane_default = cast(list[Any], d.pop("sane_default"))

        values_list = cast(list[Any], d.pop("values_list"))

        description = d.pop("description")

        multiple = d.pop("multiple")

        disable_correlation = d.pop("disable_correlation", UNSET)

        object_template_element = cls(
            id=id,
            object_template_id=object_template_id,
            object_relation=object_relation,
            type_=type_,
            ui_priority=ui_priority,
            categories=categories,
            sane_default=sane_default,
            values_list=values_list,
            description=description,
            multiple=multiple,
            disable_correlation=disable_correlation,
        )

        object_template_element.additional_properties = d
        return object_template_element

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
