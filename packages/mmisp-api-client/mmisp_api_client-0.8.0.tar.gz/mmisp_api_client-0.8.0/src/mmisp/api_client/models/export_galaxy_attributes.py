from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportGalaxyAttributes")


@_attrs_define
class ExportGalaxyAttributes:
    """
    Attributes:
        default (bool):
        distribution (str):
        custom (Union[Unset, bool]):
        format_ (Union[Unset, str]):
        download (Union[Unset, bool]):
    """

    default: bool
    distribution: str
    custom: Union[Unset, bool] = UNSET
    format_: Union[Unset, str] = UNSET
    download: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default = self.default

        distribution = self.distribution

        custom = self.custom

        format_ = self.format_

        download = self.download

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "default": default,
                "distribution": distribution,
            }
        )
        if custom is not UNSET:
            field_dict["custom"] = custom
        if format_ is not UNSET:
            field_dict["format"] = format_
        if download is not UNSET:
            field_dict["download"] = download

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        default = d.pop("default")

        distribution = d.pop("distribution")

        custom = d.pop("custom", UNSET)

        format_ = d.pop("format", UNSET)

        download = d.pop("download", UNSET)

        export_galaxy_attributes = cls(
            default=default,
            distribution=distribution,
            custom=custom,
            format_=format_,
            download=download,
        )

        export_galaxy_attributes.additional_properties = d
        return export_galaxy_attributes

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
