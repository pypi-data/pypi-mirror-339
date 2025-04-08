from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.warninglists_response import WarninglistsResponse


T = TypeVar("T", bound="GetSelectedAllWarninglistsResponse")


@_attrs_define
class GetSelectedAllWarninglistsResponse:
    """
    Attributes:
        warninglists (list['WarninglistsResponse']):
    """

    warninglists: list["WarninglistsResponse"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        warninglists = []
        for warninglists_item_data in self.warninglists:
            warninglists_item = warninglists_item_data.to_dict()
            warninglists.append(warninglists_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Warninglists": warninglists,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.warninglists_response import WarninglistsResponse

        d = dict(src_dict)
        warninglists = []
        _warninglists = d.pop("Warninglists")
        for warninglists_item_data in _warninglists:
            warninglists_item = WarninglistsResponse.from_dict(warninglists_item_data)

            warninglists.append(warninglists_item)

        get_selected_all_warninglists_response = cls(
            warninglists=warninglists,
        )

        get_selected_all_warninglists_response.additional_properties = d
        return get_selected_all_warninglists_response

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
