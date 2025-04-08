from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_attributes_model_overrides import SearchAttributesModelOverrides


T = TypeVar("T", bound="SearchAttributesBody")


@_attrs_define
class SearchAttributesBody:
    """
    Attributes:
        value (Union[Unset, str]):
        value1 (Union[Unset, str]):
        value2 (Union[Unset, str]):
        type_ (Union[Unset, str]):
        category (Union[Unset, str]):
        org (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        last (Union[Unset, int]):
        eventid (Union[Unset, str]):
        published (Union[Unset, bool]):
        to_ids (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        return_format (Union[Unset, str]):  Default: 'json'.
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        with_attachments (Union[Unset, bool]):
        uuid (Union[Unset, str]):
        publish_timestamp (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        attribute_timestamp (Union[Unset, str]):
        enforce_warninglist (Union[Unset, bool]):
        event_timestamp (Union[Unset, str]):
        threat_level_id (Union[Unset, int]):
        eventinfo (Union[Unset, str]):
        sharinggroup (Union[Unset, list[str]]):
        decaying_model (Union[Unset, str]):
        score (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        include_event_uuid (Union[Unset, bool]):
        include_event_tags (Union[Unset, bool]):
        include_proposals (Union[Unset, bool]):
        requested_attributes (Union[Unset, list[str]]):
        include_context (Union[Unset, bool]):
        headerless (Union[Unset, bool]):
        include_warninglist_hits (Union[Unset, bool]):
        attack_galaxy (Union[Unset, str]):
        object_relation (Union[Unset, str]):
        include_sightings (Union[Unset, bool]):
        include_correlations (Union[Unset, bool]):
        model_overrides (Union[Unset, SearchAttributesModelOverrides]):
        include_decay_score (Union[Unset, bool]):
        include_full_model (Union[Unset, bool]):
        exclude_decayed (Union[Unset, bool]):
    """

    value: Union[Unset, str] = UNSET
    value1: Union[Unset, str] = UNSET
    value2: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    org: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    last: Union[Unset, int] = UNSET
    eventid: Union[Unset, str] = UNSET
    published: Union[Unset, bool] = UNSET
    to_ids: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    return_format: Union[Unset, str] = "json"
    page: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    with_attachments: Union[Unset, bool] = UNSET
    uuid: Union[Unset, str] = UNSET
    publish_timestamp: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    attribute_timestamp: Union[Unset, str] = UNSET
    enforce_warninglist: Union[Unset, bool] = UNSET
    event_timestamp: Union[Unset, str] = UNSET
    threat_level_id: Union[Unset, int] = UNSET
    eventinfo: Union[Unset, str] = UNSET
    sharinggroup: Union[Unset, list[str]] = UNSET
    decaying_model: Union[Unset, str] = UNSET
    score: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    include_event_uuid: Union[Unset, bool] = UNSET
    include_event_tags: Union[Unset, bool] = UNSET
    include_proposals: Union[Unset, bool] = UNSET
    requested_attributes: Union[Unset, list[str]] = UNSET
    include_context: Union[Unset, bool] = UNSET
    headerless: Union[Unset, bool] = UNSET
    include_warninglist_hits: Union[Unset, bool] = UNSET
    attack_galaxy: Union[Unset, str] = UNSET
    object_relation: Union[Unset, str] = UNSET
    include_sightings: Union[Unset, bool] = UNSET
    include_correlations: Union[Unset, bool] = UNSET
    model_overrides: Union[Unset, "SearchAttributesModelOverrides"] = UNSET
    include_decay_score: Union[Unset, bool] = UNSET
    include_full_model: Union[Unset, bool] = UNSET
    exclude_decayed: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        value1 = self.value1

        value2 = self.value2

        type_ = self.type_

        category = self.category

        org = self.org

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        from_ = self.from_

        to = self.to

        last = self.last

        eventid = self.eventid

        published = self.published

        to_ids = self.to_ids

        deleted = self.deleted

        return_format = self.return_format

        page = self.page

        limit = self.limit

        with_attachments = self.with_attachments

        uuid = self.uuid

        publish_timestamp = self.publish_timestamp

        timestamp = self.timestamp

        attribute_timestamp = self.attribute_timestamp

        enforce_warninglist = self.enforce_warninglist

        event_timestamp = self.event_timestamp

        threat_level_id = self.threat_level_id

        eventinfo = self.eventinfo

        sharinggroup: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sharinggroup, Unset):
            sharinggroup = self.sharinggroup

        decaying_model = self.decaying_model

        score = self.score

        first_seen = self.first_seen

        last_seen = self.last_seen

        include_event_uuid = self.include_event_uuid

        include_event_tags = self.include_event_tags

        include_proposals = self.include_proposals

        requested_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.requested_attributes, Unset):
            requested_attributes = self.requested_attributes

        include_context = self.include_context

        headerless = self.headerless

        include_warninglist_hits = self.include_warninglist_hits

        attack_galaxy = self.attack_galaxy

        object_relation = self.object_relation

        include_sightings = self.include_sightings

        include_correlations = self.include_correlations

        model_overrides: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model_overrides, Unset):
            model_overrides = self.model_overrides.to_dict()

        include_decay_score = self.include_decay_score

        include_full_model = self.include_full_model

        exclude_decayed = self.exclude_decayed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if value1 is not UNSET:
            field_dict["value1"] = value1
        if value2 is not UNSET:
            field_dict["value2"] = value2
        if type_ is not UNSET:
            field_dict["type"] = type_
        if category is not UNSET:
            field_dict["category"] = category
        if org is not UNSET:
            field_dict["org"] = org
        if tags is not UNSET:
            field_dict["tags"] = tags
        if from_ is not UNSET:
            field_dict["from_"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if last is not UNSET:
            field_dict["last"] = last
        if eventid is not UNSET:
            field_dict["eventid"] = eventid
        if published is not UNSET:
            field_dict["published"] = published
        if to_ids is not UNSET:
            field_dict["to_ids"] = to_ids
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if return_format is not UNSET:
            field_dict["returnFormat"] = return_format
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if with_attachments is not UNSET:
            field_dict["withAttachments"] = with_attachments
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if publish_timestamp is not UNSET:
            field_dict["publish_timestamp"] = publish_timestamp
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if attribute_timestamp is not UNSET:
            field_dict["attribute_timestamp"] = attribute_timestamp
        if enforce_warninglist is not UNSET:
            field_dict["enforceWarninglist"] = enforce_warninglist
        if event_timestamp is not UNSET:
            field_dict["event_timestamp"] = event_timestamp
        if threat_level_id is not UNSET:
            field_dict["threat_level_id"] = threat_level_id
        if eventinfo is not UNSET:
            field_dict["eventinfo"] = eventinfo
        if sharinggroup is not UNSET:
            field_dict["sharinggroup"] = sharinggroup
        if decaying_model is not UNSET:
            field_dict["decayingModel"] = decaying_model
        if score is not UNSET:
            field_dict["score"] = score
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if include_event_uuid is not UNSET:
            field_dict["includeEventUuid"] = include_event_uuid
        if include_event_tags is not UNSET:
            field_dict["includeEventTags"] = include_event_tags
        if include_proposals is not UNSET:
            field_dict["includeProposals"] = include_proposals
        if requested_attributes is not UNSET:
            field_dict["requested_attributes"] = requested_attributes
        if include_context is not UNSET:
            field_dict["includeContext"] = include_context
        if headerless is not UNSET:
            field_dict["headerless"] = headerless
        if include_warninglist_hits is not UNSET:
            field_dict["includeWarninglistHits"] = include_warninglist_hits
        if attack_galaxy is not UNSET:
            field_dict["attackGalaxy"] = attack_galaxy
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if include_sightings is not UNSET:
            field_dict["includeSightings"] = include_sightings
        if include_correlations is not UNSET:
            field_dict["includeCorrelations"] = include_correlations
        if model_overrides is not UNSET:
            field_dict["modelOverrides"] = model_overrides
        if include_decay_score is not UNSET:
            field_dict["includeDecayScore"] = include_decay_score
        if include_full_model is not UNSET:
            field_dict["includeFullModel"] = include_full_model
        if exclude_decayed is not UNSET:
            field_dict["excludeDecayed"] = exclude_decayed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_attributes_model_overrides import SearchAttributesModelOverrides

        d = dict(src_dict)
        value = d.pop("value", UNSET)

        value1 = d.pop("value1", UNSET)

        value2 = d.pop("value2", UNSET)

        type_ = d.pop("type", UNSET)

        category = d.pop("category", UNSET)

        org = d.pop("org", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        from_ = d.pop("from_", UNSET)

        to = d.pop("to", UNSET)

        last = d.pop("last", UNSET)

        eventid = d.pop("eventid", UNSET)

        published = d.pop("published", UNSET)

        to_ids = d.pop("to_ids", UNSET)

        deleted = d.pop("deleted", UNSET)

        return_format = d.pop("returnFormat", UNSET)

        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        with_attachments = d.pop("withAttachments", UNSET)

        uuid = d.pop("uuid", UNSET)

        publish_timestamp = d.pop("publish_timestamp", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        attribute_timestamp = d.pop("attribute_timestamp", UNSET)

        enforce_warninglist = d.pop("enforceWarninglist", UNSET)

        event_timestamp = d.pop("event_timestamp", UNSET)

        threat_level_id = d.pop("threat_level_id", UNSET)

        eventinfo = d.pop("eventinfo", UNSET)

        sharinggroup = cast(list[str], d.pop("sharinggroup", UNSET))

        decaying_model = d.pop("decayingModel", UNSET)

        score = d.pop("score", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        include_event_uuid = d.pop("includeEventUuid", UNSET)

        include_event_tags = d.pop("includeEventTags", UNSET)

        include_proposals = d.pop("includeProposals", UNSET)

        requested_attributes = cast(list[str], d.pop("requested_attributes", UNSET))

        include_context = d.pop("includeContext", UNSET)

        headerless = d.pop("headerless", UNSET)

        include_warninglist_hits = d.pop("includeWarninglistHits", UNSET)

        attack_galaxy = d.pop("attackGalaxy", UNSET)

        object_relation = d.pop("object_relation", UNSET)

        include_sightings = d.pop("includeSightings", UNSET)

        include_correlations = d.pop("includeCorrelations", UNSET)

        _model_overrides = d.pop("modelOverrides", UNSET)
        model_overrides: Union[Unset, SearchAttributesModelOverrides]
        if isinstance(_model_overrides, Unset):
            model_overrides = UNSET
        else:
            model_overrides = SearchAttributesModelOverrides.from_dict(_model_overrides)

        include_decay_score = d.pop("includeDecayScore", UNSET)

        include_full_model = d.pop("includeFullModel", UNSET)

        exclude_decayed = d.pop("excludeDecayed", UNSET)

        search_attributes_body = cls(
            value=value,
            value1=value1,
            value2=value2,
            type_=type_,
            category=category,
            org=org,
            tags=tags,
            from_=from_,
            to=to,
            last=last,
            eventid=eventid,
            published=published,
            to_ids=to_ids,
            deleted=deleted,
            return_format=return_format,
            page=page,
            limit=limit,
            with_attachments=with_attachments,
            uuid=uuid,
            publish_timestamp=publish_timestamp,
            timestamp=timestamp,
            attribute_timestamp=attribute_timestamp,
            enforce_warninglist=enforce_warninglist,
            event_timestamp=event_timestamp,
            threat_level_id=threat_level_id,
            eventinfo=eventinfo,
            sharinggroup=sharinggroup,
            decaying_model=decaying_model,
            score=score,
            first_seen=first_seen,
            last_seen=last_seen,
            include_event_uuid=include_event_uuid,
            include_event_tags=include_event_tags,
            include_proposals=include_proposals,
            requested_attributes=requested_attributes,
            include_context=include_context,
            headerless=headerless,
            include_warninglist_hits=include_warninglist_hits,
            attack_galaxy=attack_galaxy,
            object_relation=object_relation,
            include_sightings=include_sightings,
            include_correlations=include_correlations,
            model_overrides=model_overrides,
            include_decay_score=include_decay_score,
            include_full_model=include_full_model,
            exclude_decayed=exclude_decayed,
        )

        search_attributes_body.additional_properties = d
        return search_attributes_body

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
