from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddAuthKeyResponseAuthKey")


@_attrs_define
class AddAuthKeyResponseAuthKey:
    """
    Attributes:
        id (int):
        uuid (str):
        authkey_start (str):
        authkey_end (str):
        created (str):
        read_only (bool):
        user_id (int):
        unique_ips (list[str]):
        authkey_raw (str):
        expiration (Union[Unset, str]):  Default: '0'.
        comment (Union[Unset, str]):
        allowed_ips (Union[Unset, list[str]]):
    """

    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    read_only: bool
    user_id: int
    unique_ips: list[str]
    authkey_raw: str
    expiration: Union[Unset, str] = "0"
    comment: Union[Unset, str] = UNSET
    allowed_ips: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        authkey_start = self.authkey_start

        authkey_end = self.authkey_end

        created = self.created

        read_only = self.read_only

        user_id = self.user_id

        unique_ips = self.unique_ips

        authkey_raw = self.authkey_raw

        expiration = self.expiration

        comment = self.comment

        allowed_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "authkey_start": authkey_start,
                "authkey_end": authkey_end,
                "created": created,
                "read_only": read_only,
                "user_id": user_id,
                "unique_ips": unique_ips,
                "authkey_raw": authkey_raw,
            }
        )
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if comment is not UNSET:
            field_dict["comment"] = comment
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        authkey_start = d.pop("authkey_start")

        authkey_end = d.pop("authkey_end")

        created = d.pop("created")

        read_only = d.pop("read_only")

        user_id = d.pop("user_id")

        unique_ips = cast(list[str], d.pop("unique_ips"))

        authkey_raw = d.pop("authkey_raw")

        expiration = d.pop("expiration", UNSET)

        comment = d.pop("comment", UNSET)

        allowed_ips = cast(list[str], d.pop("allowed_ips", UNSET))

        add_auth_key_response_auth_key = cls(
            id=id,
            uuid=uuid,
            authkey_start=authkey_start,
            authkey_end=authkey_end,
            created=created,
            read_only=read_only,
            user_id=user_id,
            unique_ips=unique_ips,
            authkey_raw=authkey_raw,
            expiration=expiration,
            comment=comment,
            allowed_ips=allowed_ips,
        )

        add_auth_key_response_auth_key.additional_properties = d
        return add_auth_key_response_auth_key

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
