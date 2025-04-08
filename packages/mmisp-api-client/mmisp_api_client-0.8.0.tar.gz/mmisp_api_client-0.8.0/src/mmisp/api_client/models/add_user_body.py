from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddUserBody")


@_attrs_define
class AddUserBody:
    """
    Attributes:
        authkey (str):
        contactalert (bool):
        nids_sid (int):
        org_id (int):
        email (str):
        termsaccepted (bool):
        disabled (bool):
        notification_daily (bool):
        notification_weekly (bool):
        notification_monthly (bool):
        password (str):
        name (str):
        role_id (str):
    """

    authkey: str
    contactalert: bool
    nids_sid: int
    org_id: int
    email: str
    termsaccepted: bool
    disabled: bool
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    password: str
    name: str
    role_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        authkey = self.authkey

        contactalert = self.contactalert

        nids_sid = self.nids_sid

        org_id = self.org_id

        email = self.email

        termsaccepted = self.termsaccepted

        disabled = self.disabled

        notification_daily = self.notification_daily

        notification_weekly = self.notification_weekly

        notification_monthly = self.notification_monthly

        password = self.password

        name = self.name

        role_id = self.role_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "authkey": authkey,
                "contactalert": contactalert,
                "nids_sid": nids_sid,
                "org_id": org_id,
                "email": email,
                "termsaccepted": termsaccepted,
                "disabled": disabled,
                "notification_daily": notification_daily,
                "notification_weekly": notification_weekly,
                "notification_monthly": notification_monthly,
                "password": password,
                "name": name,
                "role_id": role_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        authkey = d.pop("authkey")

        contactalert = d.pop("contactalert")

        nids_sid = d.pop("nids_sid")

        org_id = d.pop("org_id")

        email = d.pop("email")

        termsaccepted = d.pop("termsaccepted")

        disabled = d.pop("disabled")

        notification_daily = d.pop("notification_daily")

        notification_weekly = d.pop("notification_weekly")

        notification_monthly = d.pop("notification_monthly")

        password = d.pop("password")

        name = d.pop("name")

        role_id = d.pop("role_id")

        add_user_body = cls(
            authkey=authkey,
            contactalert=contactalert,
            nids_sid=nids_sid,
            org_id=org_id,
            email=email,
            termsaccepted=termsaccepted,
            disabled=disabled,
            notification_daily=notification_daily,
            notification_weekly=notification_weekly,
            notification_monthly=notification_monthly,
            password=password,
            name=name,
            role_id=role_id,
        )

        add_user_body.additional_properties = d
        return add_user_body

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
