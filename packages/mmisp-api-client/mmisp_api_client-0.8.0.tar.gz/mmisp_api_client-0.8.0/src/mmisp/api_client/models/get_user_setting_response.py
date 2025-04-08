from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetUserSettingResponse")


@_attrs_define
class GetUserSettingResponse:
    """
    Attributes:
        id (int):
        setting (str):
        value (str):
        user_id (int):
        timestamp (str):
    """

    id: int
    setting: str
    value: str
    user_id: int
    timestamp: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        setting = self.setting

        value = self.value

        user_id = self.user_id

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "setting": setting,
                "value": value,
                "user_id": user_id,
                "timestamp": timestamp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        setting = d.pop("setting")

        value = d.pop("value")

        user_id = d.pop("user_id")

        timestamp = d.pop("timestamp")

        get_user_setting_response = cls(
            id=id,
            setting=setting,
            value=value,
            user_id=user_id,
            timestamp=timestamp,
        )

        get_user_setting_response.additional_properties = d
        return get_user_setting_response

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
