from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.login_type import LoginType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.identity_provider_info import IdentityProviderInfo


T = TypeVar("T", bound="StartLoginResponse")


@_attrs_define
class StartLoginResponse:
    """
    Attributes:
        login_type (LoginType): An enumeration.
        identity_providers (Union[Unset, list['IdentityProviderInfo']]):
    """

    login_type: LoginType
    identity_providers: Union[Unset, list["IdentityProviderInfo"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        login_type = self.login_type.value

        identity_providers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.identity_providers, Unset):
            identity_providers = []
            for identity_providers_item_data in self.identity_providers:
                identity_providers_item = identity_providers_item_data.to_dict()
                identity_providers.append(identity_providers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "loginType": login_type,
            }
        )
        if identity_providers is not UNSET:
            field_dict["identityProviders"] = identity_providers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.identity_provider_info import IdentityProviderInfo

        d = dict(src_dict)
        login_type = LoginType(d.pop("loginType"))

        identity_providers = []
        _identity_providers = d.pop("identityProviders", UNSET)
        for identity_providers_item_data in _identity_providers or []:
            identity_providers_item = IdentityProviderInfo.from_dict(identity_providers_item_data)

            identity_providers.append(identity_providers_item)

        start_login_response = cls(
            login_type=login_type,
            identity_providers=identity_providers,
        )

        start_login_response.additional_properties = d
        return start_login_response

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
