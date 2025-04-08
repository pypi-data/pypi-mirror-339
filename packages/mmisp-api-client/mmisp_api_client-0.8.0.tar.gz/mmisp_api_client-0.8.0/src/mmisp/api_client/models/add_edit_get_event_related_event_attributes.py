from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.add_edit_get_event_related_event_attributes_org import AddEditGetEventRelatedEventAttributesOrg


T = TypeVar("T", bound="AddEditGetEventRelatedEventAttributes")


@_attrs_define
class AddEditGetEventRelatedEventAttributes:
    """
    Attributes:
        id (int):
        date (str):
        threat_level_id (int):
        info (str):
        published (str):
        uuid (str):
        analysis (str):
        timestamp (str):
        distribution (str):
        org_id (int):
        orgc_id (int):
        org (AddEditGetEventRelatedEventAttributesOrg):
        orgc (AddEditGetEventRelatedEventAttributesOrg):
    """

    id: int
    date: str
    threat_level_id: int
    info: str
    published: str
    uuid: str
    analysis: str
    timestamp: str
    distribution: str
    org_id: int
    orgc_id: int
    org: "AddEditGetEventRelatedEventAttributesOrg"
    orgc: "AddEditGetEventRelatedEventAttributesOrg"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        date = self.date

        threat_level_id = self.threat_level_id

        info = self.info

        published = self.published

        uuid = self.uuid

        analysis = self.analysis

        timestamp = self.timestamp

        distribution = self.distribution

        org_id = self.org_id

        orgc_id = self.orgc_id

        org = self.org.to_dict()

        orgc = self.orgc.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "date": date,
                "threat_level_id": threat_level_id,
                "info": info,
                "published": published,
                "uuid": uuid,
                "analysis": analysis,
                "timestamp": timestamp,
                "distribution": distribution,
                "org_id": org_id,
                "orgc_id": orgc_id,
                "Org": org,
                "Orgc": orgc,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_related_event_attributes_org import AddEditGetEventRelatedEventAttributesOrg

        d = dict(src_dict)
        id = d.pop("id")

        date = d.pop("date")

        threat_level_id = d.pop("threat_level_id")

        info = d.pop("info")

        published = d.pop("published")

        uuid = d.pop("uuid")

        analysis = d.pop("analysis")

        timestamp = d.pop("timestamp")

        distribution = d.pop("distribution")

        org_id = d.pop("org_id")

        orgc_id = d.pop("orgc_id")

        org = AddEditGetEventRelatedEventAttributesOrg.from_dict(d.pop("Org"))

        orgc = AddEditGetEventRelatedEventAttributesOrg.from_dict(d.pop("Orgc"))

        add_edit_get_event_related_event_attributes = cls(
            id=id,
            date=date,
            threat_level_id=threat_level_id,
            info=info,
            published=published,
            uuid=uuid,
            analysis=analysis,
            timestamp=timestamp,
            distribution=distribution,
            org_id=org_id,
            orgc_id=orgc_id,
            org=org,
            orgc=orgc,
        )

        add_edit_get_event_related_event_attributes.additional_properties = d
        return add_edit_get_event_related_event_attributes

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
