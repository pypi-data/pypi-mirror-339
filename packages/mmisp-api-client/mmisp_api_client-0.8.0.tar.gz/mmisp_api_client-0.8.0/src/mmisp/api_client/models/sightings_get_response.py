from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sighting_attributes_response import SightingAttributesResponse


T = TypeVar("T", bound="SightingsGetResponse")


@_attrs_define
class SightingsGetResponse:
    """
    Attributes:
        sightings (list['SightingAttributesResponse']):
    """

    sightings: list["SightingAttributesResponse"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sightings = []
        for sightings_item_data in self.sightings:
            sightings_item = sightings_item_data.to_dict()
            sightings.append(sightings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sightings": sightings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sighting_attributes_response import SightingAttributesResponse

        d = dict(src_dict)
        sightings = []
        _sightings = d.pop("sightings")
        for sightings_item_data in _sightings:
            sightings_item = SightingAttributesResponse.from_dict(sightings_item_data)

            sightings.append(sightings_item)

        sightings_get_response = cls(
            sightings=sightings,
        )

        sightings_get_response.additional_properties = d
        return sightings_get_response

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
