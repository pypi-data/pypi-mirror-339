from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchUserSettingBody")


@_attrs_define
class SearchUserSettingBody:
    """
    Attributes:
        id (Union[Unset, int]):
        setting (Union[Unset, str]):
        user_id (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    setting: Union[Unset, str] = UNSET
    user_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        setting = self.setting

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if setting is not UNSET:
            field_dict["setting"] = setting
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        setting = d.pop("setting", UNSET)

        user_id = d.pop("user_id", UNSET)

        search_user_setting_body = cls(
            id=id,
            setting=setting,
            user_id=user_id,
        )

        search_user_setting_body.additional_properties = d
        return search_user_setting_body

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
