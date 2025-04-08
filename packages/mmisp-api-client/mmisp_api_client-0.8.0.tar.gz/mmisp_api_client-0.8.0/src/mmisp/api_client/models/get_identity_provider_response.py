from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetIdentityProviderResponse")


@_attrs_define
class GetIdentityProviderResponse:
    """
    Attributes:
        id (int):
        name (str):
        org_id (int):
        active (bool):
        base_url (str):
        client_id (str):
        scope (Union[Unset, str]):
    """

    id: int
    name: str
    org_id: int
    active: bool
    base_url: str
    client_id: str
    scope: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        org_id = self.org_id

        active = self.active

        base_url = self.base_url

        client_id = self.client_id

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "org_id": org_id,
                "active": active,
                "base_url": base_url,
                "client_id": client_id,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        org_id = d.pop("org_id")

        active = d.pop("active")

        base_url = d.pop("base_url")

        client_id = d.pop("client_id")

        scope = d.pop("scope", UNSET)

        get_identity_provider_response = cls(
            id=id,
            name=name,
            org_id=org_id,
            active=active,
            base_url=base_url,
            client_id=client_id,
            scope=scope,
        )

        get_identity_provider_response.additional_properties = d
        return get_identity_provider_response

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
