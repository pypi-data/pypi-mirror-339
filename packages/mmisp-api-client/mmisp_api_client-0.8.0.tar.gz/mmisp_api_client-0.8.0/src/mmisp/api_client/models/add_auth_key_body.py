from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddAuthKeyBody")


@_attrs_define
class AddAuthKeyBody:
    """
    Attributes:
        uuid (Union[Unset, str]):
        read_only (Union[Unset, bool]):
        user_id (Union[Unset, int]):
        comment (Union[Unset, str]):
        allowed_ips (Union[Unset, list[str]]):
        expiration (Union[Unset, int, str]):  Default: 0.
    """

    uuid: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    user_id: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    allowed_ips: Union[Unset, list[str]] = UNSET
    expiration: Union[Unset, int, str] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        read_only = self.read_only

        user_id = self.user_id

        comment = self.comment

        allowed_ips: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        expiration: Union[Unset, int, str]
        if isinstance(self.expiration, Unset):
            expiration = UNSET
        else:
            expiration = self.expiration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if read_only is not UNSET:
            field_dict["read_only"] = read_only
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if expiration is not UNSET:
            field_dict["expiration"] = expiration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid", UNSET)

        read_only = d.pop("read_only", UNSET)

        user_id = d.pop("user_id", UNSET)

        comment = d.pop("comment", UNSET)

        allowed_ips = cast(list[str], d.pop("allowed_ips", UNSET))

        def _parse_expiration(data: object) -> Union[Unset, int, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, int, str], data)

        expiration = _parse_expiration(d.pop("expiration", UNSET))

        add_auth_key_body = cls(
            uuid=uuid,
            read_only=read_only,
            user_id=user_id,
            comment=comment,
            allowed_ips=allowed_ips,
            expiration=expiration,
        )

        add_auth_key_body.additional_properties = d
        return add_auth_key_body

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
