from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_all_events_event_tag import GetAllEventsEventTag
    from ..models.get_all_events_galaxy_cluster import GetAllEventsGalaxyCluster
    from ..models.get_all_events_org import GetAllEventsOrg
    from ..models.minimal_sharing_group import MinimalSharingGroup


T = TypeVar("T", bound="GetAllEventsResponse")


@_attrs_define
class GetAllEventsResponse:
    """
    Attributes:
        id (int):
        org_id (int):
        distribution (str):
        info (str):
        orgc_id (int):
        uuid (str):
        date (str):
        published (bool):
        analysis (str):
        attribute_count (str):
        timestamp (str):
        sharing_group_id (int):
        proposal_email_lock (bool):
        locked (bool):
        threat_level_id (int):
        publish_timestamp (str):
        sighting_timestamp (str):
        disable_correlation (bool):
        extends_uuid (str):
        org (GetAllEventsOrg):
        orgc (GetAllEventsOrg):
        galaxy_cluster (list['GetAllEventsGalaxyCluster']):
        event_tag (list['GetAllEventsEventTag']):
        event_creator_email (Union[Unset, str]):
        protected (Union[Unset, bool]):
        sharing_group (Union[Unset, MinimalSharingGroup]):
    """

    id: int
    org_id: int
    distribution: str
    info: str
    orgc_id: int
    uuid: str
    date: str
    published: bool
    analysis: str
    attribute_count: str
    timestamp: str
    sharing_group_id: int
    proposal_email_lock: bool
    locked: bool
    threat_level_id: int
    publish_timestamp: str
    sighting_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    org: "GetAllEventsOrg"
    orgc: "GetAllEventsOrg"
    galaxy_cluster: list["GetAllEventsGalaxyCluster"]
    event_tag: list["GetAllEventsEventTag"]
    event_creator_email: Union[Unset, str] = UNSET
    protected: Union[Unset, bool] = UNSET
    sharing_group: Union[Unset, "MinimalSharingGroup"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        distribution = self.distribution

        info = self.info

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

        org = self.org.to_dict()

        orgc = self.orgc.to_dict()

        galaxy_cluster = []
        for galaxy_cluster_item_data in self.galaxy_cluster:
            galaxy_cluster_item = galaxy_cluster_item_data.to_dict()
            galaxy_cluster.append(galaxy_cluster_item)

        event_tag = []
        for event_tag_item_data in self.event_tag:
            event_tag_item = event_tag_item_data.to_dict()
            event_tag.append(event_tag_item)

        event_creator_email = self.event_creator_email

        protected = self.protected

        sharing_group: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sharing_group, Unset):
            sharing_group = self.sharing_group.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "distribution": distribution,
                "info": info,
                "orgc_id": orgc_id,
                "uuid": uuid,
                "date": date,
                "published": published,
                "analysis": analysis,
                "attribute_count": attribute_count,
                "timestamp": timestamp,
                "sharing_group_id": sharing_group_id,
                "proposal_email_lock": proposal_email_lock,
                "locked": locked,
                "threat_level_id": threat_level_id,
                "publish_timestamp": publish_timestamp,
                "sighting_timestamp": sighting_timestamp,
                "disable_correlation": disable_correlation,
                "extends_uuid": extends_uuid,
                "Org": org,
                "Orgc": orgc,
                "GalaxyCluster": galaxy_cluster,
                "EventTag": event_tag,
            }
        )
        if event_creator_email is not UNSET:
            field_dict["event_creator_email"] = event_creator_email
        if protected is not UNSET:
            field_dict["protected"] = protected
        if sharing_group is not UNSET:
            field_dict["SharingGroup"] = sharing_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_all_events_event_tag import GetAllEventsEventTag
        from ..models.get_all_events_galaxy_cluster import GetAllEventsGalaxyCluster
        from ..models.get_all_events_org import GetAllEventsOrg
        from ..models.minimal_sharing_group import MinimalSharingGroup

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        distribution = d.pop("distribution")

        info = d.pop("info")

        orgc_id = d.pop("orgc_id")

        uuid = d.pop("uuid")

        date = d.pop("date")

        published = d.pop("published")

        analysis = d.pop("analysis")

        attribute_count = d.pop("attribute_count")

        timestamp = d.pop("timestamp")

        sharing_group_id = d.pop("sharing_group_id")

        proposal_email_lock = d.pop("proposal_email_lock")

        locked = d.pop("locked")

        threat_level_id = d.pop("threat_level_id")

        publish_timestamp = d.pop("publish_timestamp")

        sighting_timestamp = d.pop("sighting_timestamp")

        disable_correlation = d.pop("disable_correlation")

        extends_uuid = d.pop("extends_uuid")

        org = GetAllEventsOrg.from_dict(d.pop("Org"))

        orgc = GetAllEventsOrg.from_dict(d.pop("Orgc"))

        galaxy_cluster = []
        _galaxy_cluster = d.pop("GalaxyCluster")
        for galaxy_cluster_item_data in _galaxy_cluster:
            galaxy_cluster_item = GetAllEventsGalaxyCluster.from_dict(galaxy_cluster_item_data)

            galaxy_cluster.append(galaxy_cluster_item)

        event_tag = []
        _event_tag = d.pop("EventTag")
        for event_tag_item_data in _event_tag:
            event_tag_item = GetAllEventsEventTag.from_dict(event_tag_item_data)

            event_tag.append(event_tag_item)

        event_creator_email = d.pop("event_creator_email", UNSET)

        protected = d.pop("protected", UNSET)

        _sharing_group = d.pop("SharingGroup", UNSET)
        sharing_group: Union[Unset, MinimalSharingGroup]
        if isinstance(_sharing_group, Unset):
            sharing_group = UNSET
        else:
            sharing_group = MinimalSharingGroup.from_dict(_sharing_group)

        get_all_events_response = cls(
            id=id,
            org_id=org_id,
            distribution=distribution,
            info=info,
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
            org=org,
            orgc=orgc,
            galaxy_cluster=galaxy_cluster,
            event_tag=event_tag,
            event_creator_email=event_creator_email,
            protected=protected,
            sharing_group=sharing_group,
        )

        get_all_events_response.additional_properties = d
        return get_all_events_response

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
