import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        id (int):
        org_id (int):
        email (str):
        autoalert (bool):
        invited_by (int):
        termsaccepted (bool):
        role_id (int):
        change_pw (bool):
        contactalert (bool):
        disabled (bool):
        current_login (int):
        last_login (int):
        force_logout (bool):
        date_created (int):
        date_modified (int):
        external_auth_required (bool):
        last_api_access (int):
        notification_daily (bool):
        notification_weekly (bool):
        notification_monthly (bool):
        gpgkey (Union[Unset, str]):
        certif_public (Union[Unset, str]):
        expiration (Union[Unset, datetime.datetime, int]):
        external_auth_key (Union[Unset, str]):
        totp (Union[Unset, str]):
        hotp_counter (Union[Unset, int]):
        last_pw_change (Union[Unset, int]):
    """

    id: int
    org_id: int
    email: str
    autoalert: bool
    invited_by: int
    termsaccepted: bool
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    current_login: int
    last_login: int
    force_logout: bool
    date_created: int
    date_modified: int
    external_auth_required: bool
    last_api_access: int
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    gpgkey: Union[Unset, str] = UNSET
    certif_public: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.datetime, int] = UNSET
    external_auth_key: Union[Unset, str] = UNSET
    totp: Union[Unset, str] = UNSET
    hotp_counter: Union[Unset, int] = UNSET
    last_pw_change: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        email = self.email

        autoalert = self.autoalert

        invited_by = self.invited_by

        termsaccepted = self.termsaccepted

        role_id = self.role_id

        change_pw = self.change_pw

        contactalert = self.contactalert

        disabled = self.disabled

        current_login = self.current_login

        last_login = self.last_login

        force_logout = self.force_logout

        date_created = self.date_created

        date_modified = self.date_modified

        external_auth_required = self.external_auth_required

        last_api_access = self.last_api_access

        notification_daily = self.notification_daily

        notification_weekly = self.notification_weekly

        notification_monthly = self.notification_monthly

        gpgkey = self.gpgkey

        certif_public = self.certif_public

        expiration: Union[Unset, int, str]
        if isinstance(self.expiration, Unset):
            expiration = UNSET
        elif isinstance(self.expiration, datetime.datetime):
            expiration = self.expiration.isoformat()
        else:
            expiration = self.expiration

        external_auth_key = self.external_auth_key

        totp = self.totp

        hotp_counter = self.hotp_counter

        last_pw_change = self.last_pw_change

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "email": email,
                "autoalert": autoalert,
                "invited_by": invited_by,
                "termsaccepted": termsaccepted,
                "role_id": role_id,
                "change_pw": change_pw,
                "contactalert": contactalert,
                "disabled": disabled,
                "current_login": current_login,
                "last_login": last_login,
                "force_logout": force_logout,
                "date_created": date_created,
                "date_modified": date_modified,
                "external_auth_required": external_auth_required,
                "last_api_access": last_api_access,
                "notification_daily": notification_daily,
                "notification_weekly": notification_weekly,
                "notification_monthly": notification_monthly,
            }
        )
        if gpgkey is not UNSET:
            field_dict["gpgkey"] = gpgkey
        if certif_public is not UNSET:
            field_dict["certif_public"] = certif_public
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if external_auth_key is not UNSET:
            field_dict["external_auth_key"] = external_auth_key
        if totp is not UNSET:
            field_dict["totp"] = totp
        if hotp_counter is not UNSET:
            field_dict["hotp_counter"] = hotp_counter
        if last_pw_change is not UNSET:
            field_dict["last_pw_change"] = last_pw_change

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        email = d.pop("email")

        autoalert = d.pop("autoalert")

        invited_by = d.pop("invited_by")

        termsaccepted = d.pop("termsaccepted")

        role_id = d.pop("role_id")

        change_pw = d.pop("change_pw")

        contactalert = d.pop("contactalert")

        disabled = d.pop("disabled")

        current_login = d.pop("current_login")

        last_login = d.pop("last_login")

        force_logout = d.pop("force_logout")

        date_created = d.pop("date_created")

        date_modified = d.pop("date_modified")

        external_auth_required = d.pop("external_auth_required")

        last_api_access = d.pop("last_api_access")

        notification_daily = d.pop("notification_daily")

        notification_weekly = d.pop("notification_weekly")

        notification_monthly = d.pop("notification_monthly")

        gpgkey = d.pop("gpgkey", UNSET)

        certif_public = d.pop("certif_public", UNSET)

        def _parse_expiration(data: object) -> Union[Unset, datetime.datetime, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_type_0 = isoparse(data)

                return expiration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, int], data)

        expiration = _parse_expiration(d.pop("expiration", UNSET))

        external_auth_key = d.pop("external_auth_key", UNSET)

        totp = d.pop("totp", UNSET)

        hotp_counter = d.pop("hotp_counter", UNSET)

        last_pw_change = d.pop("last_pw_change", UNSET)

        user = cls(
            id=id,
            org_id=org_id,
            email=email,
            autoalert=autoalert,
            invited_by=invited_by,
            termsaccepted=termsaccepted,
            role_id=role_id,
            change_pw=change_pw,
            contactalert=contactalert,
            disabled=disabled,
            current_login=current_login,
            last_login=last_login,
            force_logout=force_logout,
            date_created=date_created,
            date_modified=date_modified,
            external_auth_required=external_auth_required,
            last_api_access=last_api_access,
            notification_daily=notification_daily,
            notification_weekly=notification_weekly,
            notification_monthly=notification_monthly,
            gpgkey=gpgkey,
            certif_public=certif_public,
            expiration=expiration,
            external_auth_key=external_auth_key,
            totp=totp,
            hotp_counter=hotp_counter,
            last_pw_change=last_pw_change,
        )

        user.additional_properties = d
        return user

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
