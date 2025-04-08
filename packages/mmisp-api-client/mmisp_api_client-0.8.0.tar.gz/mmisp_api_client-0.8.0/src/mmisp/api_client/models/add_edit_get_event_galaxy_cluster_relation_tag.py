from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddEditGetEventGalaxyClusterRelationTag")


@_attrs_define
class AddEditGetEventGalaxyClusterRelationTag:
    """
    Attributes:
        id (int):
        name (str):
        colour (str):
        exportable (bool):
        org_id (int):
        user_id (int):
        hide_tag (bool):
        numerical_value (str):
        is_galaxy (bool):
        is_custom_galaxy (bool):
        local_only (bool):
    """

    id: int
    name: str
    colour: str
    exportable: bool
    org_id: int
    user_id: int
    hide_tag: bool
    numerical_value: str
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        colour = self.colour

        exportable = self.exportable

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
                "org_id": org_id,
                "user_id": user_id,
                "hide_tag": hide_tag,
                "numerical_value": numerical_value,
                "is_galaxy": is_galaxy,
                "is_custom_galaxy": is_custom_galaxy,
                "local_only": local_only,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        colour = d.pop("colour")

        exportable = d.pop("exportable")

        org_id = d.pop("org_id")

        user_id = d.pop("user_id")

        hide_tag = d.pop("hide_tag")

        numerical_value = d.pop("numerical_value")

        is_galaxy = d.pop("is_galaxy")

        is_custom_galaxy = d.pop("is_custom_galaxy")

        local_only = d.pop("local_only")

        add_edit_get_event_galaxy_cluster_relation_tag = cls(
            id=id,
            name=name,
            colour=colour,
            exportable=exportable,
            org_id=org_id,
            user_id=user_id,
            hide_tag=hide_tag,
            numerical_value=numerical_value,
            is_galaxy=is_galaxy,
            is_custom_galaxy=is_custom_galaxy,
            local_only=local_only,
        )

        add_edit_get_event_galaxy_cluster_relation_tag.additional_properties = d
        return add_edit_get_event_galaxy_cluster_relation_tag

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
