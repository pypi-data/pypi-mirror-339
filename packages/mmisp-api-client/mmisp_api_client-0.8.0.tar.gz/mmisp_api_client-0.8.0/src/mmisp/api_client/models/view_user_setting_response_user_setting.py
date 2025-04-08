from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.view_user_setting_response_user_setting_value_type_0 import (
        ViewUserSettingResponseUserSettingValueType0,
    )


T = TypeVar("T", bound="ViewUserSettingResponseUserSetting")


@_attrs_define
class ViewUserSettingResponseUserSetting:
    """
    Attributes:
        id (int):
        setting (str):
        value (Union['ViewUserSettingResponseUserSettingValueType0', list[Any]]):
        user_id (int):
        timestamp (str):
    """

    id: int
    setting: str
    value: Union["ViewUserSettingResponseUserSettingValueType0", list[Any]]
    user_id: int
    timestamp: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.view_user_setting_response_user_setting_value_type_0 import (
            ViewUserSettingResponseUserSettingValueType0,
        )

        id = self.id

        setting = self.setting

        value: Union[dict[str, Any], list[Any]]
        if isinstance(self.value, ViewUserSettingResponseUserSettingValueType0):
            value = self.value.to_dict()
        else:
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
        from ..models.view_user_setting_response_user_setting_value_type_0 import (
            ViewUserSettingResponseUserSettingValueType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        setting = d.pop("setting")

        def _parse_value(data: object) -> Union["ViewUserSettingResponseUserSettingValueType0", list[Any]]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = ViewUserSettingResponseUserSettingValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            value_type_1 = cast(list[Any], data)

            return value_type_1

        value = _parse_value(d.pop("value"))

        user_id = d.pop("user_id")

        timestamp = d.pop("timestamp")

        view_user_setting_response_user_setting = cls(
            id=id,
            setting=setting,
            value=value,
            user_id=user_id,
            timestamp=timestamp,
        )

        view_user_setting_response_user_setting.additional_properties = d
        return view_user_setting_response_user_setting

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
