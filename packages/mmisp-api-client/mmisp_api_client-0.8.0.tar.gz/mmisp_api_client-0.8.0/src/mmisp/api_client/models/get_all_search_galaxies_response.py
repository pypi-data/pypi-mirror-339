from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_all_search_galaxies_attributes import GetAllSearchGalaxiesAttributes


T = TypeVar("T", bound="GetAllSearchGalaxiesResponse")


@_attrs_define
class GetAllSearchGalaxiesResponse:
    """
    Attributes:
        galaxy (GetAllSearchGalaxiesAttributes):
    """

    galaxy: "GetAllSearchGalaxiesAttributes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        galaxy = self.galaxy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Galaxy": galaxy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_all_search_galaxies_attributes import GetAllSearchGalaxiesAttributes

        d = dict(src_dict)
        galaxy = GetAllSearchGalaxiesAttributes.from_dict(d.pop("Galaxy"))

        get_all_search_galaxies_response = cls(
            galaxy=galaxy,
        )

        get_all_search_galaxies_response.additional_properties = d
        return get_all_search_galaxies_response

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
