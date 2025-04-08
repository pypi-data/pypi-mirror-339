from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddRemoveTagEventsResponse")


@_attrs_define
class AddRemoveTagEventsResponse:
    """
    Attributes:
        saved (bool):
        success (Union[Unset, str]):
        check_publish (Union[Unset, bool]):
        errors (Union[Unset, str]):
    """

    saved: bool
    success: Union[Unset, str] = UNSET
    check_publish: Union[Unset, bool] = UNSET
    errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        success = self.success

        check_publish = self.check_publish

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
        if check_publish is not UNSET:
            field_dict["check_publish"] = check_publish
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saved = d.pop("saved")

        success = d.pop("success", UNSET)

        check_publish = d.pop("check_publish", UNSET)

        errors = d.pop("errors", UNSET)

        add_remove_tag_events_response = cls(
            saved=saved,
            success=success,
            check_publish=check_publish,
            errors=errors,
        )

        add_remove_tag_events_response.additional_properties = d
        return add_remove_tag_events_response

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
