from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagViewResponse")


@_attrs_define
class TagViewResponse:
    """
    Attributes:
        id (int):
        name (str):
        colour (str):
        exportable (bool):
        count (int):
        attribute_count (int):
        org_id (Union[Unset, int]):
        user_id (Union[Unset, int]):
        hide_tag (Union[Unset, bool]):
        numerical_value (Union[Unset, str]):
        is_galaxy (Union[Unset, bool]):
        is_custom_galaxy (Union[Unset, bool]):
        local_only (Union[Unset, bool]):
    """

    id: int
    name: str
    colour: str
    exportable: bool
    count: int
    attribute_count: int
    org_id: Union[Unset, int] = UNSET
    user_id: Union[Unset, int] = UNSET
    hide_tag: Union[Unset, bool] = UNSET
    numerical_value: Union[Unset, str] = UNSET
    is_galaxy: Union[Unset, bool] = UNSET
    is_custom_galaxy: Union[Unset, bool] = UNSET
    local_only: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        colour = self.colour

        exportable = self.exportable

        count = self.count

        attribute_count = self.attribute_count

        org_id = self.org_id

        user_id = self.user_id

        hide_tag = self.hide_tag

        numerical_value = self.numerical_value

        is_galaxy = self.is_galaxy

        is_custom_galaxy = self.is_custom_galaxy

        local_only = self.local_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "colour": colour,
                "exportable": exportable,
                "count": count,
                "attribute_count": attribute_count,
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
        if is_galaxy is not UNSET:
            field_dict["is_galaxy"] = is_galaxy
        if is_custom_galaxy is not UNSET:
            field_dict["is_custom_galaxy"] = is_custom_galaxy
        if local_only is not UNSET:
            field_dict["local_only"] = local_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        colour = d.pop("colour")

        exportable = d.pop("exportable")

        count = d.pop("count")

        attribute_count = d.pop("attribute_count")

        org_id = d.pop("org_id", UNSET)

        user_id = d.pop("user_id", UNSET)

        hide_tag = d.pop("hide_tag", UNSET)

        numerical_value = d.pop("numerical_value", UNSET)

        is_galaxy = d.pop("is_galaxy", UNSET)

        is_custom_galaxy = d.pop("is_custom_galaxy", UNSET)

        local_only = d.pop("local_only", UNSET)

        tag_view_response = cls(
            id=id,
            name=name,
            colour=colour,
            exportable=exportable,
            count=count,
            attribute_count=attribute_count,
            org_id=org_id,
            user_id=user_id,
            hide_tag=hide_tag,
            numerical_value=numerical_value,
            is_galaxy=is_galaxy,
            is_custom_galaxy=is_custom_galaxy,
            local_only=local_only,
        )

        tag_view_response.additional_properties = d
        return tag_view_response

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
