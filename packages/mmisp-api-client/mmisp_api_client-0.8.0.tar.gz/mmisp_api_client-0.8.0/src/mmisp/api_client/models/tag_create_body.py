from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagCreateBody")


@_attrs_define
class TagCreateBody:
    """
    Attributes:
        name (str):
        colour (str):
        exportable (bool):
        org_id (Union[Unset, int]):
        user_id (Union[Unset, int]):
        hide_tag (Union[Unset, bool]):
        numerical_value (Union[Unset, str]):
        local_only (Union[Unset, bool]):
    """

    name: str
    colour: str
    exportable: bool
    org_id: Union[Unset, int] = UNSET
    user_id: Union[Unset, int] = UNSET
    hide_tag: Union[Unset, bool] = UNSET
    numerical_value: Union[Unset, str] = UNSET
    local_only: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        colour = self.colour

        exportable = self.exportable

        org_id = self.org_id

        user_id = self.user_id

        hide_tag = self.hide_tag

        numerical_value = self.numerical_value

        local_only = self.local_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "colour": colour,
                "exportable": exportable,
            }
        )
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if hide_tag is not UNSET:
            field_dict["hide_tag"] = hide_tag
        if numerical_value is not UNSET:
            field_dict["numerical_value"] = numerical_value
        if local_only is not UNSET:
            field_dict["local_only"] = local_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        colour = d.pop("colour")

        exportable = d.pop("exportable")

        org_id = d.pop("org_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        hide_tag = d.pop("hide_tag", UNSET)

        numerical_value = d.pop("numerical_value", UNSET)

        local_only = d.pop("local_only", UNSET)

        tag_create_body = cls(
            name=name,
            colour=colour,
            exportable=exportable,
            org_id=org_id,
            user_id=user_id,
            hide_tag=hide_tag,
            numerical_value=numerical_value,
            local_only=local_only,
        )

        tag_create_body.additional_properties = d
        return tag_create_body

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
