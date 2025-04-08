from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddEditGetEventTag")


@_attrs_define
class AddEditGetEventTag:
    """
    Attributes:
        id (int):
        name (str):
        colour (str):
        exportable (bool):
        user_id (int):
        hide_tag (bool):
        is_galaxy (bool):
        is_custom_galaxy (bool):
        local_only (bool):
        local (bool):
        numerical_value (Union[Unset, int]):
        relationship_type (Union[Unset, bool, str]):
    """

    id: int
    name: str
    colour: str
    exportable: bool
    user_id: int
    hide_tag: bool
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool
    local: bool
    numerical_value: Union[Unset, int] = UNSET
    relationship_type: Union[Unset, bool, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        colour = self.colour

        exportable = self.exportable

        user_id = self.user_id

        hide_tag = self.hide_tag

        is_galaxy = self.is_galaxy

        is_custom_galaxy = self.is_custom_galaxy

        local_only = self.local_only

        local = self.local

        numerical_value = self.numerical_value

        relationship_type: Union[Unset, bool, str]
        if isinstance(self.relationship_type, Unset):
            relationship_type = UNSET
        else:
            relationship_type = self.relationship_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "colour": colour,
                "exportable": exportable,
                "user_id": user_id,
                "hide_tag": hide_tag,
                "is_galaxy": is_galaxy,
                "is_custom_galaxy": is_custom_galaxy,
                "local_only": local_only,
                "local": local,
            }
        )
        if numerical_value is not UNSET:
            field_dict["numerical_value"] = numerical_value
        if relationship_type is not UNSET:
            field_dict["relationship_type"] = relationship_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        colour = d.pop("colour")

        exportable = d.pop("exportable")

        user_id = d.pop("user_id")

        hide_tag = d.pop("hide_tag")

        is_galaxy = d.pop("is_galaxy")

        is_custom_galaxy = d.pop("is_custom_galaxy")

        local_only = d.pop("local_only")

        local = d.pop("local")

        numerical_value = d.pop("numerical_value", UNSET)

        def _parse_relationship_type(data: object) -> Union[Unset, bool, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, bool, str], data)

        relationship_type = _parse_relationship_type(d.pop("relationship_type", UNSET))

        add_edit_get_event_tag = cls(
            id=id,
            name=name,
            colour=colour,
            exportable=exportable,
            user_id=user_id,
            hide_tag=hide_tag,
            is_galaxy=is_galaxy,
            is_custom_galaxy=is_custom_galaxy,
            local_only=local_only,
            local=local,
            numerical_value=numerical_value,
            relationship_type=relationship_type,
        )

        add_edit_get_event_tag.additional_properties = d
        return add_edit_get_event_tag

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
