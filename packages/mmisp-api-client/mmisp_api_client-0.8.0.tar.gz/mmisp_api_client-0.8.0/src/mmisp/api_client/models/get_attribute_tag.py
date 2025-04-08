from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAttributeTag")


@_attrs_define
class GetAttributeTag:
    """
    Attributes:
        id (int):
        name (str):
        colour (str):
        is_galaxy (bool):
        local (bool):
        numerical_value (Union[Unset, int]):
    """

    id: int
    name: str
    colour: str
    is_galaxy: bool
    local: bool
    numerical_value: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        colour = self.colour

        is_galaxy = self.is_galaxy

        local = self.local

        numerical_value = self.numerical_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "colour": colour,
                "is_galaxy": is_galaxy,
                "local": local,
            }
        )
        if numerical_value is not UNSET:
            field_dict["numerical_value"] = numerical_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        colour = d.pop("colour")

        is_galaxy = d.pop("is_galaxy")

        local = d.pop("local")

        numerical_value = d.pop("numerical_value", UNSET)

        get_attribute_tag = cls(
            id=id,
            name=name,
            colour=colour,
            is_galaxy=is_galaxy,
            local=local,
            numerical_value=numerical_value,
        )

        get_attribute_tag.additional_properties = d
        return get_attribute_tag

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
