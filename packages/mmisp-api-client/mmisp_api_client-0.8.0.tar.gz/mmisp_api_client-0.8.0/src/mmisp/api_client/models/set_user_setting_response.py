from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_user_setting_response_user_setting import SetUserSettingResponseUserSetting


T = TypeVar("T", bound="SetUserSettingResponse")


@_attrs_define
class SetUserSettingResponse:
    """
    Attributes:
        user_setting (SetUserSettingResponseUserSetting):
    """

    user_setting: "SetUserSettingResponseUserSetting"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_setting = self.user_setting.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "UserSetting": user_setting,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_user_setting_response_user_setting import SetUserSettingResponseUserSetting

        d = dict(src_dict)
        user_setting = SetUserSettingResponseUserSetting.from_dict(d.pop("UserSetting"))

        set_user_setting_response = cls(
            user_setting=user_setting,
        )

        set_user_setting_response.additional_properties = d
        return set_user_setting_response

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
