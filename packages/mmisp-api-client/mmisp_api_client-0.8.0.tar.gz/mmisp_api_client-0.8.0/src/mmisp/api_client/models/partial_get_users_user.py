from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialGetUsersUser")


@_attrs_define
class PartialGetUsersUser:
    """
    Attributes:
        id (Union[Unset, int]):
        org_id (Union[Unset, int]):
        server_id (Union[Unset, int]):  Default: 0.
        email (Union[Unset, str]):
        autoalert (Union[Unset, bool]):
        auth_key (Union[Unset, str]):
        invited_by (Union[Unset, int]):
        gpg_key (Union[Unset, str]):
        certif_public (Union[Unset, str]):
        nids_sid (Union[Unset, int]):
        termsaccepted (Union[Unset, bool]):
        newsread (Union[Unset, int]):
        role_id (Union[Unset, int]):
        change_pw (Union[Unset, bool]):
        contactalert (Union[Unset, bool]):
        disabled (Union[Unset, bool]):
        expiration (Union[Unset, int]):
        current_login (Union[Unset, int]):
        last_login (Union[Unset, int]):
        last_api_access (Union[Unset, int]):
        force_logout (Union[Unset, bool]):
        date_created (Union[Unset, int]):
        date_modified (Union[Unset, int]):
        last_pw_change (Union[Unset, int]):
        totp (Union[Unset, str]):
        hotp_counter (Union[Unset, int]):
        notification_daily (Union[Unset, bool]):
        notification_weekly (Union[Unset, bool]):
        notification_monthly (Union[Unset, bool]):
        external_auth_required (Union[Unset, bool]):
        external_auth_key (Union[Unset, str]):
        sub (Union[Unset, str]):
        name (Union[Unset, str]):
        contact (Union[Unset, bool]):
        notification (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    org_id: Union[Unset, int] = UNSET
    server_id: Union[Unset, int] = 0
    email: Union[Unset, str] = UNSET
    autoalert: Union[Unset, bool] = UNSET
    auth_key: Union[Unset, str] = UNSET
    invited_by: Union[Unset, int] = UNSET
    gpg_key: Union[Unset, str] = UNSET
    certif_public: Union[Unset, str] = UNSET
    nids_sid: Union[Unset, int] = UNSET
    termsaccepted: Union[Unset, bool] = UNSET
    newsread: Union[Unset, int] = UNSET
    role_id: Union[Unset, int] = UNSET
    change_pw: Union[Unset, bool] = UNSET
    contactalert: Union[Unset, bool] = UNSET
    disabled: Union[Unset, bool] = UNSET
    expiration: Union[Unset, int] = UNSET
    current_login: Union[Unset, int] = UNSET
    last_login: Union[Unset, int] = UNSET
    last_api_access: Union[Unset, int] = UNSET
    force_logout: Union[Unset, bool] = UNSET
    date_created: Union[Unset, int] = UNSET
    date_modified: Union[Unset, int] = UNSET
    last_pw_change: Union[Unset, int] = UNSET
    totp: Union[Unset, str] = UNSET
    hotp_counter: Union[Unset, int] = UNSET
    notification_daily: Union[Unset, bool] = UNSET
    notification_weekly: Union[Unset, bool] = UNSET
    notification_monthly: Union[Unset, bool] = UNSET
    external_auth_required: Union[Unset, bool] = UNSET
    external_auth_key: Union[Unset, str] = UNSET
    sub: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    contact: Union[Unset, bool] = UNSET
    notification: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        server_id = self.server_id

        email = self.email

        autoalert = self.autoalert

        auth_key = self.auth_key

        invited_by = self.invited_by

        gpg_key = self.gpg_key

        certif_public = self.certif_public

        nids_sid = self.nids_sid

        termsaccepted = self.termsaccepted

        newsread = self.newsread

        role_id = self.role_id

        change_pw = self.change_pw

        contactalert = self.contactalert

        disabled = self.disabled

        expiration = self.expiration

        current_login = self.current_login

        last_login = self.last_login

        last_api_access = self.last_api_access

        force_logout = self.force_logout

        date_created = self.date_created

        date_modified = self.date_modified

        last_pw_change = self.last_pw_change

        totp = self.totp

        hotp_counter = self.hotp_counter

        notification_daily = self.notification_daily

        notification_weekly = self.notification_weekly

        notification_monthly = self.notification_monthly

        external_auth_required = self.external_auth_required

        external_auth_key = self.external_auth_key

        sub = self.sub

        name = self.name

        contact = self.contact

        notification = self.notification

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if email is not UNSET:
            field_dict["email"] = email
        if autoalert is not UNSET:
            field_dict["autoalert"] = autoalert
        if auth_key is not UNSET:
            field_dict["auth_key"] = auth_key
        if invited_by is not UNSET:
            field_dict["invited_by"] = invited_by
        if gpg_key is not UNSET:
            field_dict["gpg_key"] = gpg_key
        if certif_public is not UNSET:
            field_dict["certif_public"] = certif_public
        if nids_sid is not UNSET:
            field_dict["nids_sid"] = nids_sid
        if termsaccepted is not UNSET:
            field_dict["termsaccepted"] = termsaccepted
        if newsread is not UNSET:
            field_dict["newsread"] = newsread
        if role_id is not UNSET:
            field_dict["role_id"] = role_id
        if change_pw is not UNSET:
            field_dict["change_pw"] = change_pw
        if contactalert is not UNSET:
            field_dict["contactalert"] = contactalert
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if current_login is not UNSET:
            field_dict["current_login"] = current_login
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if last_api_access is not UNSET:
            field_dict["last_api_access"] = last_api_access
        if force_logout is not UNSET:
            field_dict["force_logout"] = force_logout
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if date_modified is not UNSET:
            field_dict["date_modified"] = date_modified
        if last_pw_change is not UNSET:
            field_dict["last_pw_change"] = last_pw_change
        if totp is not UNSET:
            field_dict["totp"] = totp
        if hotp_counter is not UNSET:
            field_dict["hotp_counter"] = hotp_counter
        if notification_daily is not UNSET:
            field_dict["notification_daily"] = notification_daily
        if notification_weekly is not UNSET:
            field_dict["notification_weekly"] = notification_weekly
        if notification_monthly is not UNSET:
            field_dict["notification_monthly"] = notification_monthly
        if external_auth_required is not UNSET:
            field_dict["external_auth_required"] = external_auth_required
        if external_auth_key is not UNSET:
            field_dict["external_auth_key"] = external_auth_key
        if sub is not UNSET:
            field_dict["sub"] = sub
        if name is not UNSET:
            field_dict["name"] = name
        if contact is not UNSET:
            field_dict["contact"] = contact
        if notification is not UNSET:
            field_dict["notification"] = notification

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        org_id = d.pop("org_id", UNSET)

        server_id = d.pop("server_id", UNSET)

        email = d.pop("email", UNSET)

        autoalert = d.pop("autoalert", UNSET)

        auth_key = d.pop("auth_key", UNSET)

        invited_by = d.pop("invited_by", UNSET)

        gpg_key = d.pop("gpg_key", UNSET)

        certif_public = d.pop("certif_public", UNSET)

        nids_sid = d.pop("nids_sid", UNSET)

        termsaccepted = d.pop("termsaccepted", UNSET)

        newsread = d.pop("newsread", UNSET)

        role_id = d.pop("role_id", UNSET)

        change_pw = d.pop("change_pw", UNSET)

        contactalert = d.pop("contactalert", UNSET)

        disabled = d.pop("disabled", UNSET)

        expiration = d.pop("expiration", UNSET)

        current_login = d.pop("current_login", UNSET)

        last_login = d.pop("last_login", UNSET)

        last_api_access = d.pop("last_api_access", UNSET)

        force_logout = d.pop("force_logout", UNSET)

        date_created = d.pop("date_created", UNSET)

        date_modified = d.pop("date_modified", UNSET)

        last_pw_change = d.pop("last_pw_change", UNSET)

        totp = d.pop("totp", UNSET)

        hotp_counter = d.pop("hotp_counter", UNSET)

        notification_daily = d.pop("notification_daily", UNSET)

        notification_weekly = d.pop("notification_weekly", UNSET)

        notification_monthly = d.pop("notification_monthly", UNSET)

        external_auth_required = d.pop("external_auth_required", UNSET)

        external_auth_key = d.pop("external_auth_key", UNSET)

        sub = d.pop("sub", UNSET)

        name = d.pop("name", UNSET)

        contact = d.pop("contact", UNSET)

        notification = d.pop("notification", UNSET)

        partial_get_users_user = cls(
            id=id,
            org_id=org_id,
            server_id=server_id,
            email=email,
            autoalert=autoalert,
            auth_key=auth_key,
            invited_by=invited_by,
            gpg_key=gpg_key,
            certif_public=certif_public,
            nids_sid=nids_sid,
            termsaccepted=termsaccepted,
            newsread=newsread,
            role_id=role_id,
            change_pw=change_pw,
            contactalert=contactalert,
            disabled=disabled,
            expiration=expiration,
            current_login=current_login,
            last_login=last_login,
            last_api_access=last_api_access,
            force_logout=force_logout,
            date_created=date_created,
            date_modified=date_modified,
            last_pw_change=last_pw_change,
            totp=totp,
            hotp_counter=hotp_counter,
            notification_daily=notification_daily,
            notification_weekly=notification_weekly,
            notification_monthly=notification_monthly,
            external_auth_required=external_auth_required,
            external_auth_key=external_auth_key,
            sub=sub,
            name=name,
            contact=contact,
            notification=notification,
        )

        partial_get_users_user.additional_properties = d
        return partial_get_users_user

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
