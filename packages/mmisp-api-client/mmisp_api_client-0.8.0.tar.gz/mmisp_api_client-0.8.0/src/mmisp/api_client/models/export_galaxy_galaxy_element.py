from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportGalaxyGalaxyElement")


@_attrs_define
class ExportGalaxyGalaxyElement:
    """
    Attributes:
        key (str):
        value (str):
        id (Union[Unset, int]):
        galaxy_cluster_id (Union[Unset, int]):
    """

    key: str
    value: str
    id: Union[Unset, int] = UNSET
    galaxy_cluster_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value

        id = self.id

        galaxy_cluster_id = self.galaxy_cluster_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if galaxy_cluster_id is not UNSET:
            field_dict["galaxy_cluster_id"] = galaxy_cluster_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        value = d.pop("value")

        id = d.pop("id", UNSET)

        galaxy_cluster_id = d.pop("galaxy_cluster_id", UNSET)

        export_galaxy_galaxy_element = cls(
            key=key,
            value=value,
            id=id,
            galaxy_cluster_id=galaxy_cluster_id,
        )

        export_galaxy_galaxy_element.additional_properties = d
        return export_galaxy_galaxy_element

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
