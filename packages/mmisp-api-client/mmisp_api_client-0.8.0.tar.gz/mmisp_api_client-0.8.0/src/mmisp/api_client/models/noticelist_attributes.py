from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NoticelistAttributes")


@_attrs_define
class NoticelistAttributes:
    """
    Attributes:
        id (int):
        name (str):
        expanded_name (str):
        ref (list[str]):
        geographical_area (list[str]):
        version (str):
        enabled (bool):
    """

    id: int
    name: str
    expanded_name: str
    ref: list[str]
    geographical_area: list[str]
    version: str
    enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        expanded_name = self.expanded_name

        ref = self.ref

        geographical_area = self.geographical_area

        version = self.version

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "expanded_name": expanded_name,
                "ref": ref,
                "geographical_area": geographical_area,
                "version": version,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        expanded_name = d.pop("expanded_name")

        ref = cast(list[str], d.pop("ref"))

        geographical_area = cast(list[str], d.pop("geographical_area"))

        version = d.pop("version")

        enabled = d.pop("enabled")

        noticelist_attributes = cls(
            id=id,
            name=name,
            expanded_name=expanded_name,
            ref=ref,
            geographical_area=geographical_area,
            version=version,
            enabled=enabled,
        )

        noticelist_attributes.additional_properties = d
        return noticelist_attributes

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
