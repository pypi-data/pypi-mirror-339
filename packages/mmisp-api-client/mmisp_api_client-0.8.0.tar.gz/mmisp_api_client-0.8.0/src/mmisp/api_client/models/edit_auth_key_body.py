from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditAuthKeyBody")


@_attrs_define
class EditAuthKeyBody:
    """
    Attributes:
        read_only (Union[Unset, bool]):
        comment (Union[Unset, str]):
        allowed_ips (Union[Unset, list[str], str]):
        expiration (Union[Unset, str]):
    """

    read_only: Union[Unset, bool] = UNSET
    comment: Union[Unset, str] = UNSET
    allowed_ips: Union[Unset, list[str], str] = UNSET
    expiration: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        read_only = self.read_only

        comment = self.comment

        allowed_ips: Union[Unset, list[str], str]
        if isinstance(self.allowed_ips, Unset):
            allowed_ips = UNSET
        elif isinstance(self.allowed_ips, list):
            allowed_ips = self.allowed_ips

        else:
            allowed_ips = self.allowed_ips

        expiration = self.expiration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if read_only is not UNSET:
            field_dict["read_only"] = read_only
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
        read_only = d.pop("read_only", UNSET)

        comment = d.pop("comment", UNSET)

        def _parse_allowed_ips(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_ips_type_1 = cast(list[str], data)

                return allowed_ips_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        allowed_ips = _parse_allowed_ips(d.pop("allowed_ips", UNSET))

        expiration = d.pop("expiration", UNSET)

        edit_auth_key_body = cls(
            read_only=read_only,
            comment=comment,
            allowed_ips=allowed_ips,
            expiration=expiration,
        )

        edit_auth_key_body.additional_properties = d
        return edit_auth_key_body

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
