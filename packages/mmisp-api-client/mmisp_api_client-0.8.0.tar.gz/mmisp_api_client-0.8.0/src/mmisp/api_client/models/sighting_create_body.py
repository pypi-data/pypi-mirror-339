from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sighting_filters_body import SightingFiltersBody


T = TypeVar("T", bound="SightingCreateBody")


@_attrs_define
class SightingCreateBody:
    """
    Attributes:
        values (list[str]):
        source (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        filters (Union[Unset, SightingFiltersBody]):
    """

    values: list[str]
    source: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    filters: Union[Unset, "SightingFiltersBody"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        values = self.values

        source = self.source

        timestamp = self.timestamp

        filters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "values": values,
            }
        )
        if source is not UNSET:
            field_dict["source"] = source
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sighting_filters_body import SightingFiltersBody

        d = dict(src_dict)
        values = cast(list[str], d.pop("values"))

        source = d.pop("source", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        _filters = d.pop("filters", UNSET)
        filters: Union[Unset, SightingFiltersBody]
        if isinstance(_filters, Unset):
            filters = UNSET
        else:
            filters = SightingFiltersBody.from_dict(_filters)

        sighting_create_body = cls(
            values=values,
            source=source,
            timestamp=timestamp,
            filters=filters,
        )

        sighting_create_body.additional_properties = d
        return sighting_create_body

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
