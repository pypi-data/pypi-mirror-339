from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IdentityProviderEditBody")


@_attrs_define
class IdentityProviderEditBody:
    """
    Attributes:
        name (Union[Unset, str]):
        org_id (Union[Unset, int]):
        active (Union[Unset, bool]):
        base_url (Union[Unset, str]):
        client_id (Union[Unset, str]):
        client_secret (Union[Unset, str]):
        scope (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    org_id: Union[Unset, int] = UNSET
    active: Union[Unset, bool] = UNSET
    base_url: Union[Unset, str] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_secret: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        org_id = self.org_id

        active = self.active

        base_url = self.base_url

        client_id = self.client_id

        client_secret = self.client_secret

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if active is not UNSET:
            field_dict["active"] = active
        if base_url is not UNSET:
            field_dict["base_url"] = base_url
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        org_id = d.pop("org_id", UNSET)

        active = d.pop("active", UNSET)

        base_url = d.pop("base_url", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        scope = d.pop("scope", UNSET)

        identity_provider_edit_body = cls(
            name=name,
            org_id=org_id,
            active=active,
            base_url=base_url,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
        )

        identity_provider_edit_body.additional_properties = d
        return identity_provider_edit_body

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
