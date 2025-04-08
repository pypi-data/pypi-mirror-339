from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_attribute import AddEditGetEventAttribute
    from ..models.add_edit_get_event_event_report import AddEditGetEventEventReport
    from ..models.add_edit_get_event_galaxy import AddEditGetEventGalaxy
    from ..models.add_edit_get_event_object import AddEditGetEventObject
    from ..models.add_edit_get_event_org import AddEditGetEventOrg
    from ..models.add_edit_get_event_related_event import AddEditGetEventRelatedEvent
    from ..models.add_edit_get_event_shadow_attribute import AddEditGetEventShadowAttribute
    from ..models.add_edit_get_event_tag import AddEditGetEventTag
    from ..models.event_sharing_group_response import EventSharingGroupResponse


T = TypeVar("T", bound="AddEditGetEventDetails")


@_attrs_define
class AddEditGetEventDetails:
    """
    Attributes:
        id (int):
        orgc_id (int):
        org_id (int):
        date (str):
        threat_level_id (int):
        info (str):
        published (bool):
        uuid (str):
        attribute_count (str):
        analysis (str):
        timestamp (str):
        distribution (int):
        proposal_email_lock (bool):
        locked (bool):
        publish_timestamp (str):
        disable_correlation (bool):
        extends_uuid (str):
        org (AddEditGetEventOrg):
        orgc (AddEditGetEventOrg):
        sharing_group_id (Union[Unset, int]):
        protected (Union[Unset, bool]):
        event_creator_email (Union[Unset, str]):
        attribute (Union[Unset, list['AddEditGetEventAttribute']]):
        shadow_attribute (Union[Unset, list['AddEditGetEventShadowAttribute']]):
        related_event (Union[Unset, list['AddEditGetEventRelatedEvent']]):
        galaxy (Union[Unset, list['AddEditGetEventGalaxy']]):
        object_ (Union[Unset, list['AddEditGetEventObject']]):
        event_report (Union[Unset, list['AddEditGetEventEventReport']]):
        cryptographic_key (Union[Unset, list[str]]):
        tag (Union[Unset, list['AddEditGetEventTag']]):
        sharing_group (Union[Unset, EventSharingGroupResponse]):
    """

    id: int
    orgc_id: int
    org_id: int
    date: str
    threat_level_id: int
    info: str
    published: bool
    uuid: str
    attribute_count: str
    analysis: str
    timestamp: str
    distribution: int
    proposal_email_lock: bool
    locked: bool
    publish_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    org: "AddEditGetEventOrg"
    orgc: "AddEditGetEventOrg"
    sharing_group_id: Union[Unset, int] = UNSET
    protected: Union[Unset, bool] = UNSET
    event_creator_email: Union[Unset, str] = UNSET
    attribute: Union[Unset, list["AddEditGetEventAttribute"]] = UNSET
    shadow_attribute: Union[Unset, list["AddEditGetEventShadowAttribute"]] = UNSET
    related_event: Union[Unset, list["AddEditGetEventRelatedEvent"]] = UNSET
    galaxy: Union[Unset, list["AddEditGetEventGalaxy"]] = UNSET
    object_: Union[Unset, list["AddEditGetEventObject"]] = UNSET
    event_report: Union[Unset, list["AddEditGetEventEventReport"]] = UNSET
    cryptographic_key: Union[Unset, list[str]] = UNSET
    tag: Union[Unset, list["AddEditGetEventTag"]] = UNSET
    sharing_group: Union[Unset, "EventSharingGroupResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        orgc_id = self.orgc_id

        org_id = self.org_id

        date = self.date

        threat_level_id = self.threat_level_id

        info = self.info

        published = self.published

        uuid = self.uuid

        attribute_count = self.attribute_count

        analysis = self.analysis

        timestamp = self.timestamp

        distribution = self.distribution

        proposal_email_lock = self.proposal_email_lock

        locked = self.locked

        publish_timestamp = self.publish_timestamp

        disable_correlation = self.disable_correlation

        extends_uuid = self.extends_uuid

        org = self.org.to_dict()

        orgc = self.orgc.to_dict()

        sharing_group_id = self.sharing_group_id

        protected = self.protected

        event_creator_email = self.event_creator_email

        attribute: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attribute, Unset):
            attribute = []
            for attribute_item_data in self.attribute:
                attribute_item = attribute_item_data.to_dict()
                attribute.append(attribute_item)

        shadow_attribute: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.shadow_attribute, Unset):
            shadow_attribute = []
            for shadow_attribute_item_data in self.shadow_attribute:
                shadow_attribute_item = shadow_attribute_item_data.to_dict()
                shadow_attribute.append(shadow_attribute_item)

        related_event: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.related_event, Unset):
            related_event = []
            for related_event_item_data in self.related_event:
                related_event_item = related_event_item_data.to_dict()
                related_event.append(related_event_item)

        galaxy: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.galaxy, Unset):
            galaxy = []
            for galaxy_item_data in self.galaxy:
                galaxy_item = galaxy_item_data.to_dict()
                galaxy.append(galaxy_item)

        object_: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = []
            for object_item_data in self.object_:
                object_item = object_item_data.to_dict()
                object_.append(object_item)

        event_report: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.event_report, Unset):
            event_report = []
            for event_report_item_data in self.event_report:
                event_report_item = event_report_item_data.to_dict()
                event_report.append(event_report_item)

        cryptographic_key: Union[Unset, list[str]] = UNSET
        if not isinstance(self.cryptographic_key, Unset):
            cryptographic_key = self.cryptographic_key

        tag: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = []
            for tag_item_data in self.tag:
                tag_item = tag_item_data.to_dict()
                tag.append(tag_item)

        sharing_group: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sharing_group, Unset):
            sharing_group = self.sharing_group.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "orgc_id": orgc_id,
                "org_id": org_id,
                "date": date,
                "threat_level_id": threat_level_id,
                "info": info,
                "published": published,
                "uuid": uuid,
                "attribute_count": attribute_count,
                "analysis": analysis,
                "timestamp": timestamp,
                "distribution": distribution,
                "proposal_email_lock": proposal_email_lock,
                "locked": locked,
                "publish_timestamp": publish_timestamp,
                "disable_correlation": disable_correlation,
                "extends_uuid": extends_uuid,
                "Org": org,
                "Orgc": orgc,
            }
        )
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if protected is not UNSET:
            field_dict["protected"] = protected
        if event_creator_email is not UNSET:
            field_dict["event_creator_email"] = event_creator_email
        if attribute is not UNSET:
            field_dict["Attribute"] = attribute
        if shadow_attribute is not UNSET:
            field_dict["ShadowAttribute"] = shadow_attribute
        if related_event is not UNSET:
            field_dict["RelatedEvent"] = related_event
        if galaxy is not UNSET:
            field_dict["Galaxy"] = galaxy
        if object_ is not UNSET:
            field_dict["Object"] = object_
        if event_report is not UNSET:
            field_dict["EventReport"] = event_report
        if cryptographic_key is not UNSET:
            field_dict["CryptographicKey"] = cryptographic_key
        if tag is not UNSET:
            field_dict["Tag"] = tag
        if sharing_group is not UNSET:
            field_dict["SharingGroup"] = sharing_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_attribute import AddEditGetEventAttribute
        from ..models.add_edit_get_event_event_report import AddEditGetEventEventReport
        from ..models.add_edit_get_event_galaxy import AddEditGetEventGalaxy
        from ..models.add_edit_get_event_object import AddEditGetEventObject
        from ..models.add_edit_get_event_org import AddEditGetEventOrg
        from ..models.add_edit_get_event_related_event import AddEditGetEventRelatedEvent
        from ..models.add_edit_get_event_shadow_attribute import AddEditGetEventShadowAttribute
        from ..models.add_edit_get_event_tag import AddEditGetEventTag
        from ..models.event_sharing_group_response import EventSharingGroupResponse

        d = dict(src_dict)
        id = d.pop("id")

        orgc_id = d.pop("orgc_id")

        org_id = d.pop("org_id")

        date = d.pop("date")

        threat_level_id = d.pop("threat_level_id")

        info = d.pop("info")

        published = d.pop("published")

        uuid = d.pop("uuid")

        attribute_count = d.pop("attribute_count")

        analysis = d.pop("analysis")

        timestamp = d.pop("timestamp")

        distribution = d.pop("distribution")

        proposal_email_lock = d.pop("proposal_email_lock")

        locked = d.pop("locked")

        publish_timestamp = d.pop("publish_timestamp")

        disable_correlation = d.pop("disable_correlation")

        extends_uuid = d.pop("extends_uuid")

        org = AddEditGetEventOrg.from_dict(d.pop("Org"))

        orgc = AddEditGetEventOrg.from_dict(d.pop("Orgc"))

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        protected = d.pop("protected", UNSET)

        event_creator_email = d.pop("event_creator_email", UNSET)

        attribute = []
        _attribute = d.pop("Attribute", UNSET)
        for attribute_item_data in _attribute or []:
            attribute_item = AddEditGetEventAttribute.from_dict(attribute_item_data)

            attribute.append(attribute_item)

        shadow_attribute = []
        _shadow_attribute = d.pop("ShadowAttribute", UNSET)
        for shadow_attribute_item_data in _shadow_attribute or []:
            shadow_attribute_item = AddEditGetEventShadowAttribute.from_dict(shadow_attribute_item_data)

            shadow_attribute.append(shadow_attribute_item)

        related_event = []
        _related_event = d.pop("RelatedEvent", UNSET)
        for related_event_item_data in _related_event or []:
            related_event_item = AddEditGetEventRelatedEvent.from_dict(related_event_item_data)

            related_event.append(related_event_item)

        galaxy = []
        _galaxy = d.pop("Galaxy", UNSET)
        for galaxy_item_data in _galaxy or []:
            galaxy_item = AddEditGetEventGalaxy.from_dict(galaxy_item_data)

            galaxy.append(galaxy_item)

        object_ = []
        _object_ = d.pop("Object", UNSET)
        for object_item_data in _object_ or []:
            object_item = AddEditGetEventObject.from_dict(object_item_data)

            object_.append(object_item)

        event_report = []
        _event_report = d.pop("EventReport", UNSET)
        for event_report_item_data in _event_report or []:
            event_report_item = AddEditGetEventEventReport.from_dict(event_report_item_data)

            event_report.append(event_report_item)

        cryptographic_key = cast(list[str], d.pop("CryptographicKey", UNSET))

        tag = []
        _tag = d.pop("Tag", UNSET)
        for tag_item_data in _tag or []:
            tag_item = AddEditGetEventTag.from_dict(tag_item_data)

            tag.append(tag_item)

        _sharing_group = d.pop("SharingGroup", UNSET)
        sharing_group: Union[Unset, EventSharingGroupResponse]
        if isinstance(_sharing_group, Unset):
            sharing_group = UNSET
        else:
            sharing_group = EventSharingGroupResponse.from_dict(_sharing_group)

        add_edit_get_event_details = cls(
            id=id,
            orgc_id=orgc_id,
            org_id=org_id,
            date=date,
            threat_level_id=threat_level_id,
            info=info,
            published=published,
            uuid=uuid,
            attribute_count=attribute_count,
            analysis=analysis,
            timestamp=timestamp,
            distribution=distribution,
            proposal_email_lock=proposal_email_lock,
            locked=locked,
            publish_timestamp=publish_timestamp,
            disable_correlation=disable_correlation,
            extends_uuid=extends_uuid,
            org=org,
            orgc=orgc,
            sharing_group_id=sharing_group_id,
            protected=protected,
            event_creator_email=event_creator_email,
            attribute=attribute,
            shadow_attribute=shadow_attribute,
            related_event=related_event,
            galaxy=galaxy,
            object_=object_,
            event_report=event_report,
            cryptographic_key=cryptographic_key,
            tag=tag,
            sharing_group=sharing_group,
        )

        add_edit_get_event_details.additional_properties = d
        return add_edit_get_event_details

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
