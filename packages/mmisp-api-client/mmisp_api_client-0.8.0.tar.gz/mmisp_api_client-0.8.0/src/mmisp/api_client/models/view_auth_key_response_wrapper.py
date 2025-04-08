from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ViewAuthKeyResponseWrapper")


@_attrs_define
class ViewAuthKeyResponseWrapper:
    """
    Attributes:
        id (int):
        uuid (str):
        authkey_start (str):
        authkey_end (str):
        created (str):
        expiration (int):
        read_only (bool):
        user_id (int):
        comment (str):
        allowed_ips (Union[Unset, list[str]]):
        unique_ips (Union[Unset, list[str]]):
    """

    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: int
    read_only: bool
    user_id: int
    comment: str
    allowed_ips: Union[Unset, list[str]] = UNSET
    unique_ips: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        authkey_start = self.authkey_start

        authkey_end = self.authkey_end

        created = self.created

        expiration = self.expiration

        read_only = self.read_only

        user_id = self.user_id

        comment = self.comment

        allowed_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        unique_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.unique_ips, Unset):
            unique_ips = self.unique_ips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "authkey_start": authkey_start,
                "authkey_end": authkey_end,
                "created": created,
                "expiration": expiration,
                "read_only": read_only,
                "user_id": user_id,
                "comment": comment,
            }
        )
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if unique_ips is not UNSET:
            field_dict["unique_ips"] = unique_ips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        authkey_start = d.pop("authkey_start")

        authkey_end = d.pop("authkey_end")

        created = d.pop("created")

        expiration = d.pop("expiration")

        read_only = d.pop("read_only")

        user_id = d.pop("user_id")

        comment = d.pop("comment")

        allowed_ips = cast(list[str], d.pop("allowed_ips", UNSET))

        unique_ips = cast(list[str], d.pop("unique_ips", UNSET))

        view_auth_key_response_wrapper = cls(
            id=id,
            uuid=uuid,
            authkey_start=authkey_start,
            authkey_end=authkey_end,
            created=created,
            expiration=expiration,
            read_only=read_only,
            user_id=user_id,
            comment=comment,
            allowed_ips=allowed_ips,
            unique_ips=unique_ips,
        )

        view_auth_key_response_wrapper.additional_properties = d
        return view_auth_key_response_wrapper

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
