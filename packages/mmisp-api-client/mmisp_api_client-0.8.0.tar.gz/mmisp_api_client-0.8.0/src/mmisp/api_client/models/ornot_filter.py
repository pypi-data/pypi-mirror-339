from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ORNOTFilter")


@_attrs_define
class ORNOTFilter:
    """
    Attributes:
        or_ (list[Any]):
        not_ (list[Any]):
    """

    or_: list[Any]
    not_: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        or_ = self.or_

        not_ = self.not_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "OR": or_,
                "NOT": not_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        or_ = cast(list[Any], d.pop("OR"))

        not_ = cast(list[Any], d.pop("NOT"))

        ornot_filter = cls(
            or_=or_,
            not_=not_,
        )

        ornot_filter.additional_properties = d
        return ornot_filter

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
