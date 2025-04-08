from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchAuthKeyBody")


@_attrs_define
class SearchAuthKeyBody:
    """
    Attributes:
        page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 25.
        id (Union[Unset, int]):
        uuid (Union[Unset, str]):
        authkey_start (Union[Unset, str]):
        authkey_end (Union[Unset, str]):
        created (Union[Unset, str]):
        expiration (Union[Unset, str]):
        read_only (Union[Unset, bool]):
        user_id (Union[Unset, int]):
        comment (Union[Unset, str]):
        allowed_ips (Union[Unset, list[str], str]):
        last_used (Union[Unset, str]):
    """

    page: Union[Unset, int] = 1
    limit: Union[Unset, int] = 25
    id: Union[Unset, int] = UNSET
    uuid: Union[Unset, str] = UNSET
    authkey_start: Union[Unset, str] = UNSET
    authkey_end: Union[Unset, str] = UNSET
    created: Union[Unset, str] = UNSET
    expiration: Union[Unset, str] = UNSET
    read_only: Union[Unset, bool] = UNSET
    user_id: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    allowed_ips: Union[Unset, list[str], str] = UNSET
    last_used: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        limit = self.limit

        id = self.id

        uuid = self.uuid

        authkey_start = self.authkey_start

        authkey_end = self.authkey_end

        created = self.created

        expiration = self.expiration

        read_only = self.read_only

        user_id = self.user_id

        comment = self.comment

        allowed_ips: Union[Unset, list[str], str]
        if isinstance(self.allowed_ips, Unset):
            allowed_ips = UNSET
        elif isinstance(self.allowed_ips, list):
            allowed_ips = self.allowed_ips

        else:
            allowed_ips = self.allowed_ips

        last_used = self.last_used

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if id is not UNSET:
            field_dict["id"] = id
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if authkey_start is not UNSET:
            field_dict["authkey_start"] = authkey_start
        if authkey_end is not UNSET:
            field_dict["authkey_end"] = authkey_end
        if created is not UNSET:
            field_dict["created"] = created
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if read_only is not UNSET:
            field_dict["read_only"] = read_only
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if last_used is not UNSET:
            field_dict["last_used"] = last_used

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        id = d.pop("id", UNSET)

        uuid = d.pop("uuid", UNSET)

        authkey_start = d.pop("authkey_start", UNSET)

        authkey_end = d.pop("authkey_end", UNSET)

        created = d.pop("created", UNSET)

        expiration = d.pop("expiration", UNSET)

        read_only = d.pop("read_only", UNSET)

        user_id = d.pop("user_id", UNSET)

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

        last_used = d.pop("last_used", UNSET)

        search_auth_key_body = cls(
            page=page,
            limit=limit,
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
            last_used=last_used,
        )

        search_auth_key_body.additional_properties = d
        return search_auth_key_body

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
