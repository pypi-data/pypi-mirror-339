from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.warninglist_attributes_response import WarninglistAttributesResponse


T = TypeVar("T", bound="WarninglistResponse")


@_attrs_define
class WarninglistResponse:
    """
    Attributes:
        warninglist (WarninglistAttributesResponse):
    """

    warninglist: "WarninglistAttributesResponse"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        warninglist = self.warninglist.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Warninglist": warninglist,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.warninglist_attributes_response import WarninglistAttributesResponse

        d = dict(src_dict)
        warninglist = WarninglistAttributesResponse.from_dict(d.pop("Warninglist"))

        warninglist_response = cls(
            warninglist=warninglist,
        )

        warninglist_response.additional_properties = d
        return warninglist_response

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
