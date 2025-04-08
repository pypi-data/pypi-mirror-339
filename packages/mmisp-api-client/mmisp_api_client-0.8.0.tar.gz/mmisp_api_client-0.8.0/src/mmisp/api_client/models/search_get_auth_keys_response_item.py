from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.search_get_auth_keys_response_item_auth_key import SearchGetAuthKeysResponseItemAuthKey
    from ..models.search_get_auth_keys_response_item_user import SearchGetAuthKeysResponseItemUser


T = TypeVar("T", bound="SearchGetAuthKeysResponseItem")


@_attrs_define
class SearchGetAuthKeysResponseItem:
    """
    Attributes:
        auth_key (SearchGetAuthKeysResponseItemAuthKey):
        user (SearchGetAuthKeysResponseItemUser):
    """

    auth_key: "SearchGetAuthKeysResponseItemAuthKey"
    user: "SearchGetAuthKeysResponseItemUser"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auth_key = self.auth_key.to_dict()

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "AuthKey": auth_key,
                "User": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_get_auth_keys_response_item_auth_key import SearchGetAuthKeysResponseItemAuthKey
        from ..models.search_get_auth_keys_response_item_user import SearchGetAuthKeysResponseItemUser

        d = dict(src_dict)
        auth_key = SearchGetAuthKeysResponseItemAuthKey.from_dict(d.pop("AuthKey"))

        user = SearchGetAuthKeysResponseItemUser.from_dict(d.pop("User"))

        search_get_auth_keys_response_item = cls(
            auth_key=auth_key,
            user=user,
        )

        search_get_auth_keys_response_item.additional_properties = d
        return search_get_auth_keys_response_item

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
