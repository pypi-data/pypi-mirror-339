from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.set_user_setting_body_value_type_0 import SetUserSettingBodyValueType0


T = TypeVar("T", bound="SetUserSettingBody")


@_attrs_define
class SetUserSettingBody:
    """
    Attributes:
        value (Union['SetUserSettingBodyValueType0', list[Any]]):
    """

    value: Union["SetUserSettingBodyValueType0", list[Any]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.set_user_setting_body_value_type_0 import SetUserSettingBodyValueType0

        value: Union[dict[str, Any], list[Any]]
        if isinstance(self.value, SetUserSettingBodyValueType0):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_user_setting_body_value_type_0 import SetUserSettingBodyValueType0

        d = dict(src_dict)

        def _parse_value(data: object) -> Union["SetUserSettingBodyValueType0", list[Any]]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = SetUserSettingBodyValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            value_type_1 = cast(list[Any], data)

            return value_type_1

        value = _parse_value(d.pop("value"))

        set_user_setting_body = cls(
            value=value,
        )

        set_user_setting_body.additional_properties = d
        return set_user_setting_body

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
