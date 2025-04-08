from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditEventBody")


@_attrs_define
class EditEventBody:
    """
    Attributes:
        info (Union[Unset, str]):
        org_id (Union[Unset, int]):
        distribution (Union[Unset, str]):
        orgc_id (Union[Unset, int]):
        uuid (Union[Unset, str]):
        date (Union[Unset, str]):
        published (Union[Unset, bool]):
        analysis (Union[Unset, str]):
        attribute_count (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        proposal_email_lock (Union[Unset, bool]):
        locked (Union[Unset, bool]):
        threat_level_id (Union[Unset, int]):
        publish_timestamp (Union[Unset, str]):
        sighting_timestamp (Union[Unset, str]):
        disable_correlation (Union[Unset, bool]):
        extends_uuid (Union[Unset, str]):
        event_creator_email (Union[Unset, str]):
        protected (Union[Unset, bool]):
        cryptographic_key (Union[Unset, str]):
    """

    info: Union[Unset, str] = UNSET
    org_id: Union[Unset, int] = UNSET
    distribution: Union[Unset, str] = UNSET
    orgc_id: Union[Unset, int] = UNSET
    uuid: Union[Unset, str] = UNSET
    date: Union[Unset, str] = UNSET
    published: Union[Unset, bool] = UNSET
    analysis: Union[Unset, str] = UNSET
    attribute_count: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    proposal_email_lock: Union[Unset, bool] = UNSET
    locked: Union[Unset, bool] = UNSET
    threat_level_id: Union[Unset, int] = UNSET
    publish_timestamp: Union[Unset, str] = UNSET
    sighting_timestamp: Union[Unset, str] = UNSET
    disable_correlation: Union[Unset, bool] = UNSET
    extends_uuid: Union[Unset, str] = UNSET
    event_creator_email: Union[Unset, str] = UNSET
    protected: Union[Unset, bool] = UNSET
    cryptographic_key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        info = self.info

        org_id = self.org_id

        distribution = self.distribution

        orgc_id = self.orgc_id

        uuid = self.uuid

        date = self.date

        published = self.published

        analysis = self.analysis

        attribute_count = self.attribute_count

        timestamp = self.timestamp

        sharing_group_id = self.sharing_group_id

        proposal_email_lock = self.proposal_email_lock

        locked = self.locked

        threat_level_id = self.threat_level_id

        publish_timestamp = self.publish_timestamp

        sighting_timestamp = self.sighting_timestamp

        disable_correlation = self.disable_correlation

        extends_uuid = self.extends_uuid

        event_creator_email = self.event_creator_email

        protected = self.protected

        cryptographic_key = self.cryptographic_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if info is not UNSET:
            field_dict["info"] = info
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if orgc_id is not UNSET:
            field_dict["orgc_id"] = orgc_id
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if date is not UNSET:
            field_dict["date"] = date
        if published is not UNSET:
            field_dict["published"] = published
        if analysis is not UNSET:
            field_dict["analysis"] = analysis
        if attribute_count is not UNSET:
            field_dict["attribute_count"] = attribute_count
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if proposal_email_lock is not UNSET:
            field_dict["proposal_email_lock"] = proposal_email_lock
        if locked is not UNSET:
            field_dict["locked"] = locked
        if threat_level_id is not UNSET:
            field_dict["threat_level_id"] = threat_level_id
        if publish_timestamp is not UNSET:
            field_dict["publish_timestamp"] = publish_timestamp
        if sighting_timestamp is not UNSET:
            field_dict["sighting_timestamp"] = sighting_timestamp
        if disable_correlation is not UNSET:
            field_dict["disable_correlation"] = disable_correlation
        if extends_uuid is not UNSET:
            field_dict["extends_uuid"] = extends_uuid
        if event_creator_email is not UNSET:
            field_dict["event_creator_email"] = event_creator_email
        if protected is not UNSET:
            field_dict["protected"] = protected
        if cryptographic_key is not UNSET:
            field_dict["cryptographic_key"] = cryptographic_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        info = d.pop("info", UNSET)

        org_id = d.pop("org_id", UNSET)

        distribution = d.pop("distribution", UNSET)

        orgc_id = d.pop("orgc_id", UNSET)

        uuid = d.pop("uuid", UNSET)

        date = d.pop("date", UNSET)

        published = d.pop("published", UNSET)

        analysis = d.pop("analysis", UNSET)

        attribute_count = d.pop("attribute_count", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        proposal_email_lock = d.pop("proposal_email_lock", UNSET)

        locked = d.pop("locked", UNSET)

        threat_level_id = d.pop("threat_level_id", UNSET)

        publish_timestamp = d.pop("publish_timestamp", UNSET)

        sighting_timestamp = d.pop("sighting_timestamp", UNSET)

        disable_correlation = d.pop("disable_correlation", UNSET)

        extends_uuid = d.pop("extends_uuid", UNSET)

        event_creator_email = d.pop("event_creator_email", UNSET)

        protected = d.pop("protected", UNSET)

        cryptographic_key = d.pop("cryptographic_key", UNSET)

        edit_event_body = cls(
            info=info,
            org_id=org_id,
            distribution=distribution,
            orgc_id=orgc_id,
            uuid=uuid,
            date=date,
            published=published,
            analysis=analysis,
            attribute_count=attribute_count,
            timestamp=timestamp,
            sharing_group_id=sharing_group_id,
            proposal_email_lock=proposal_email_lock,
            locked=locked,
            threat_level_id=threat_level_id,
            publish_timestamp=publish_timestamp,
            sighting_timestamp=sighting_timestamp,
            disable_correlation=disable_correlation,
            extends_uuid=extends_uuid,
            event_creator_email=event_creator_email,
            protected=protected,
            cryptographic_key=cryptographic_key,
        )

        edit_event_body.additional_properties = d
        return edit_event_body

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
