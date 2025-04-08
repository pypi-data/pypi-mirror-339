from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ToggleEnableWarninglistsBody")


@_attrs_define
class ToggleEnableWarninglistsBody:
    """
    Attributes:
        id (Union[int, list[int]]):
        name (Union[list[str], str]):
        enabled (bool):
    """

    id: Union[int, list[int]]
    name: Union[list[str], str]
    enabled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[int, list[int]]
        if isinstance(self.id, list):
            id = self.id

        else:
            id = self.id

        name: Union[list[str], str]
        if isinstance(self.name, list):
            name = self.name

        else:
            name = self.name

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "enabled": enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_id(data: object) -> Union[int, list[int]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                id_type_1 = cast(list[int], data)

                return id_type_1
            except:  # noqa: E722
                pass
            return cast(Union[int, list[int]], data)

        id = _parse_id(d.pop("id"))

        def _parse_name(data: object) -> Union[list[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                name_type_1 = cast(list[str], data)

                return name_type_1
            except:  # noqa: E722
                pass
            return cast(Union[list[str], str], data)

        name = _parse_name(d.pop("name"))

        enabled = d.pop("enabled")

        toggle_enable_warninglists_body = cls(
            id=id,
            name=name,
            enabled=enabled,
        )

        toggle_enable_warninglists_body.additional_properties = d
        return toggle_enable_warninglists_body

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
