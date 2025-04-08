from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ToggleEnableWarninglistsResponse")


@_attrs_define
class ToggleEnableWarninglistsResponse:
    """
    Attributes:
        saved (bool):
        success (Union[Unset, str]):
        errors (Union[Unset, str]):
    """

    saved: bool
    success: Union[Unset, str] = UNSET
    errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        success = self.success

        errors = self.errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "saved": saved,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saved = d.pop("saved")

        success = d.pop("success", UNSET)

        errors = d.pop("errors", UNSET)

        toggle_enable_warninglists_response = cls(
            saved=saved,
            success=success,
            errors=errors,
        )

        toggle_enable_warninglists_response.additional_properties = d
        return toggle_enable_warninglists_response

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
