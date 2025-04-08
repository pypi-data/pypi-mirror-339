import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserAttributesBody")


@_attrs_define
class UserAttributesBody:
    """
    Attributes:
        org_id (Union[Unset, int]):
        authkey (Union[Unset, str]):
        email (Union[Unset, str]):
        autoalert (Union[Unset, bool]):
        gpgkey (Union[Unset, str]):
        certif_public (Union[Unset, str]):
        termsaccepted (Union[Unset, bool]):
        role_id (Union[Unset, str]):
        change_pw (Union[Unset, bool]):
        contactalert (Union[Unset, bool]):
        disabled (Union[Unset, bool]):
        expiration (Union[Unset, datetime.datetime, str]):
        force_logout (Union[Unset, bool]):
        external_auth_required (Union[Unset, bool]):
        external_auth_key (Union[Unset, str]):
        notification_daily (Union[Unset, bool]):
        notification_weekly (Union[Unset, bool]):
        notification_monthly (Union[Unset, bool]):
        totp (Union[Unset, str]):
        hotp_counter (Union[Unset, str]):
        name (Union[Unset, str]):
        nids_sid (Union[Unset, int]):
    """

    org_id: Union[Unset, int] = UNSET
    authkey: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    autoalert: Union[Unset, bool] = UNSET
    gpgkey: Union[Unset, str] = UNSET
    certif_public: Union[Unset, str] = UNSET
    termsaccepted: Union[Unset, bool] = UNSET
    role_id: Union[Unset, str] = UNSET
    change_pw: Union[Unset, bool] = UNSET
    contactalert: Union[Unset, bool] = UNSET
    disabled: Union[Unset, bool] = UNSET
    expiration: Union[Unset, datetime.datetime, str] = UNSET
    force_logout: Union[Unset, bool] = UNSET
    external_auth_required: Union[Unset, bool] = UNSET
    external_auth_key: Union[Unset, str] = UNSET
    notification_daily: Union[Unset, bool] = UNSET
    notification_weekly: Union[Unset, bool] = UNSET
    notification_monthly: Union[Unset, bool] = UNSET
    totp: Union[Unset, str] = UNSET
    hotp_counter: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    nids_sid: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        org_id = self.org_id

        authkey = self.authkey

        email = self.email

        autoalert = self.autoalert

        gpgkey = self.gpgkey

        certif_public = self.certif_public

        termsaccepted = self.termsaccepted

        role_id = self.role_id

        change_pw = self.change_pw

        contactalert = self.contactalert

        disabled = self.disabled

        expiration: Union[Unset, str]
        if isinstance(self.expiration, Unset):
            expiration = UNSET
        elif isinstance(self.expiration, datetime.datetime):
            expiration = self.expiration.isoformat()
        else:
            expiration = self.expiration

        force_logout = self.force_logout

        external_auth_required = self.external_auth_required

        external_auth_key = self.external_auth_key

        notification_daily = self.notification_daily

        notification_weekly = self.notification_weekly

        notification_monthly = self.notification_monthly

        totp = self.totp

        hotp_counter = self.hotp_counter

        name = self.name

        nids_sid = self.nids_sid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if authkey is not UNSET:
            field_dict["authkey"] = authkey
        if email is not UNSET:
            field_dict["email"] = email
        if autoalert is not UNSET:
            field_dict["autoalert"] = autoalert
        if gpgkey is not UNSET:
            field_dict["gpgkey"] = gpgkey
        if certif_public is not UNSET:
            field_dict["certif_public"] = certif_public
        if termsaccepted is not UNSET:
            field_dict["termsaccepted"] = termsaccepted
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
        if force_logout is not UNSET:
            field_dict["force_logout"] = force_logout
        if external_auth_required is not UNSET:
            field_dict["external_auth_required"] = external_auth_required
        if external_auth_key is not UNSET:
            field_dict["external_auth_key"] = external_auth_key
        if notification_daily is not UNSET:
            field_dict["notification_daily"] = notification_daily
        if notification_weekly is not UNSET:
            field_dict["notification_weekly"] = notification_weekly
        if notification_monthly is not UNSET:
            field_dict["notification_monthly"] = notification_monthly
        if totp is not UNSET:
            field_dict["totp"] = totp
        if hotp_counter is not UNSET:
            field_dict["hotp_counter"] = hotp_counter
        if name is not UNSET:
            field_dict["name"] = name
        if nids_sid is not UNSET:
            field_dict["nids_sid"] = nids_sid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        org_id = d.pop("org_id", UNSET)

        authkey = d.pop("authkey", UNSET)

        email = d.pop("email", UNSET)

        autoalert = d.pop("autoalert", UNSET)

        gpgkey = d.pop("gpgkey", UNSET)

        certif_public = d.pop("certif_public", UNSET)

        termsaccepted = d.pop("termsaccepted", UNSET)

        role_id = d.pop("role_id", UNSET)

        change_pw = d.pop("change_pw", UNSET)

        contactalert = d.pop("contactalert", UNSET)

        disabled = d.pop("disabled", UNSET)

        def _parse_expiration(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_type_0 = isoparse(data)

                return expiration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        expiration = _parse_expiration(d.pop("expiration", UNSET))

        force_logout = d.pop("force_logout", UNSET)

        external_auth_required = d.pop("external_auth_required", UNSET)

        external_auth_key = d.pop("external_auth_key", UNSET)

        notification_daily = d.pop("notification_daily", UNSET)

        notification_weekly = d.pop("notification_weekly", UNSET)

        notification_monthly = d.pop("notification_monthly", UNSET)

        totp = d.pop("totp", UNSET)

        hotp_counter = d.pop("hotp_counter", UNSET)

        name = d.pop("name", UNSET)

        nids_sid = d.pop("nids_sid", UNSET)

        user_attributes_body = cls(
            org_id=org_id,
            authkey=authkey,
            email=email,
            autoalert=autoalert,
            gpgkey=gpgkey,
            certif_public=certif_public,
            termsaccepted=termsaccepted,
            role_id=role_id,
            change_pw=change_pw,
            contactalert=contactalert,
            disabled=disabled,
            expiration=expiration,
            force_logout=force_logout,
            external_auth_required=external_auth_required,
            external_auth_key=external_auth_key,
            notification_daily=notification_daily,
            notification_weekly=notification_weekly,
            notification_monthly=notification_monthly,
            totp=totp,
            hotp_counter=hotp_counter,
            name=name,
            nids_sid=nids_sid,
        )

        user_attributes_body.additional_properties = d
        return user_attributes_body

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
