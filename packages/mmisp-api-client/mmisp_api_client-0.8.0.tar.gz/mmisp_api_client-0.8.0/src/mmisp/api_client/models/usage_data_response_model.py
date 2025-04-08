from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UsageDataResponseModel")


@_attrs_define
class UsageDataResponseModel:
    """
    Attributes:
        events (int):
        attributes (int):
        event_attributes (int):
        users (int):
        users_with_gpg_keys (int):
        organisations (int):
        local_organisations (int):
        event_creator_orgs (int):
        average_users_per_org (float):
    """

    events: int
    attributes: int
    event_attributes: int
    users: int
    users_with_gpg_keys: int
    organisations: int
    local_organisations: int
    event_creator_orgs: int
    average_users_per_org: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events = self.events

        attributes = self.attributes

        event_attributes = self.event_attributes

        users = self.users

        users_with_gpg_keys = self.users_with_gpg_keys

        organisations = self.organisations

        local_organisations = self.local_organisations

        event_creator_orgs = self.event_creator_orgs

        average_users_per_org = self.average_users_per_org

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
                "attributes": attributes,
                "eventAttributes": event_attributes,
                "users": users,
                "usersWithGPGKeys": users_with_gpg_keys,
                "organisations": organisations,
                "localOrganisations": local_organisations,
                "eventCreatorOrgs": event_creator_orgs,
                "averageUsersPerOrg": average_users_per_org,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        events = d.pop("events")

        attributes = d.pop("attributes")

        event_attributes = d.pop("eventAttributes")

        users = d.pop("users")

        users_with_gpg_keys = d.pop("usersWithGPGKeys")

        organisations = d.pop("organisations")

        local_organisations = d.pop("localOrganisations")

        event_creator_orgs = d.pop("eventCreatorOrgs")

        average_users_per_org = d.pop("averageUsersPerOrg")

        usage_data_response_model = cls(
            events=events,
            attributes=attributes,
            event_attributes=event_attributes,
            users=users,
            users_with_gpg_keys=users_with_gpg_keys,
            organisations=organisations,
            local_organisations=local_organisations,
            event_creator_orgs=event_creator_orgs,
            average_users_per_org=average_users_per_org,
        )

        usage_data_response_model.additional_properties = d
        return usage_data_response_model

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
