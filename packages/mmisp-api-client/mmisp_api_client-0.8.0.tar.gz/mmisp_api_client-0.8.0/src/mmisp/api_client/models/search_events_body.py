from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchEventsBody")


@_attrs_define
class SearchEventsBody:
    """
    Attributes:
        return_format (str):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        value (Union[Unset, str]):
        type_ (Union[Unset, str]):
        category (Union[Unset, str]):
        org (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        event_tags (Union[Unset, list[str]]):
        searchall (Union[Unset, str]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        last (Union[Unset, int]):
        eventid (Union[Unset, int]):
        with_attachments (Union[Unset, bool]):
        sharinggroup (Union[Unset, list[str]]):
        metadata (Union[Unset, bool]):
        uuid (Union[Unset, str]):
        publish_timestamp (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        published (Union[Unset, bool]):
        enforce_warninglist (Union[Unset, bool]):
        sg_reference_only (Union[Unset, bool]):
        requested_attributes (Union[Unset, list[str]]):
        include_context (Union[Unset, bool]):
        headerless (Union[Unset, bool]):
        include_warninglist_hits (Union[Unset, bool]):
        attack_galaxy (Union[Unset, str]):
        to_ids (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        exclude_local_tags (Union[Unset, bool]):
        date (Union[Unset, str]):
        include_sightingdb (Union[Unset, bool]):
        tag (Union[Unset, str]):
        object_relation (Union[Unset, str]):
        threat_level_id (Union[Unset, int]):
    """

    return_format: str
    page: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    value: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    org: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    event_tags: Union[Unset, list[str]] = UNSET
    searchall: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    last: Union[Unset, int] = UNSET
    eventid: Union[Unset, int] = UNSET
    with_attachments: Union[Unset, bool] = UNSET
    sharinggroup: Union[Unset, list[str]] = UNSET
    metadata: Union[Unset, bool] = UNSET
    uuid: Union[Unset, str] = UNSET
    publish_timestamp: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    published: Union[Unset, bool] = UNSET
    enforce_warninglist: Union[Unset, bool] = UNSET
    sg_reference_only: Union[Unset, bool] = UNSET
    requested_attributes: Union[Unset, list[str]] = UNSET
    include_context: Union[Unset, bool] = UNSET
    headerless: Union[Unset, bool] = UNSET
    include_warninglist_hits: Union[Unset, bool] = UNSET
    attack_galaxy: Union[Unset, str] = UNSET
    to_ids: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    exclude_local_tags: Union[Unset, bool] = UNSET
    date: Union[Unset, str] = UNSET
    include_sightingdb: Union[Unset, bool] = UNSET
    tag: Union[Unset, str] = UNSET
    object_relation: Union[Unset, str] = UNSET
    threat_level_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return_format = self.return_format

        page = self.page

        limit = self.limit

        value = self.value

        type_ = self.type_

        category = self.category

        org = self.org

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        event_tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.event_tags, Unset):
            event_tags = self.event_tags

        searchall = self.searchall

        from_ = self.from_

        to = self.to

        last = self.last

        eventid = self.eventid

        with_attachments = self.with_attachments

        sharinggroup: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sharinggroup, Unset):
            sharinggroup = self.sharinggroup

        metadata = self.metadata

        uuid = self.uuid

        publish_timestamp = self.publish_timestamp

        timestamp = self.timestamp

        published = self.published

        enforce_warninglist = self.enforce_warninglist

        sg_reference_only = self.sg_reference_only

        requested_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.requested_attributes, Unset):
            requested_attributes = self.requested_attributes

        include_context = self.include_context

        headerless = self.headerless

        include_warninglist_hits = self.include_warninglist_hits

        attack_galaxy = self.attack_galaxy

        to_ids = self.to_ids

        deleted = self.deleted

        exclude_local_tags = self.exclude_local_tags

        date = self.date

        include_sightingdb = self.include_sightingdb

        tag = self.tag

        object_relation = self.object_relation

        threat_level_id = self.threat_level_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "returnFormat": return_format,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if value is not UNSET:
            field_dict["value"] = value
        if type_ is not UNSET:
            field_dict["type"] = type_
        if category is not UNSET:
            field_dict["category"] = category
        if org is not UNSET:
            field_dict["org"] = org
        if tags is not UNSET:
            field_dict["tags"] = tags
        if event_tags is not UNSET:
            field_dict["event_tags"] = event_tags
        if searchall is not UNSET:
            field_dict["searchall"] = searchall
        if from_ is not UNSET:
            field_dict["from_"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if last is not UNSET:
            field_dict["last"] = last
        if eventid is not UNSET:
            field_dict["eventid"] = eventid
        if with_attachments is not UNSET:
            field_dict["withAttachments"] = with_attachments
        if sharinggroup is not UNSET:
            field_dict["sharinggroup"] = sharinggroup
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if publish_timestamp is not UNSET:
            field_dict["publish_timestamp"] = publish_timestamp
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if published is not UNSET:
            field_dict["published"] = published
        if enforce_warninglist is not UNSET:
            field_dict["enforceWarninglist"] = enforce_warninglist
        if sg_reference_only is not UNSET:
            field_dict["sgReferenceOnly"] = sg_reference_only
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
        if to_ids is not UNSET:
            field_dict["to_ids"] = to_ids
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if exclude_local_tags is not UNSET:
            field_dict["excludeLocalTags"] = exclude_local_tags
        if date is not UNSET:
            field_dict["date"] = date
        if include_sightingdb is not UNSET:
            field_dict["includeSightingdb"] = include_sightingdb
        if tag is not UNSET:
            field_dict["tag"] = tag
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if threat_level_id is not UNSET:
            field_dict["threat_level_id"] = threat_level_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        return_format = d.pop("returnFormat")

        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        value = d.pop("value", UNSET)

        type_ = d.pop("type", UNSET)

        category = d.pop("category", UNSET)

        org = d.pop("org", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        event_tags = cast(list[str], d.pop("event_tags", UNSET))

        searchall = d.pop("searchall", UNSET)

        from_ = d.pop("from_", UNSET)

        to = d.pop("to", UNSET)

        last = d.pop("last", UNSET)

        eventid = d.pop("eventid", UNSET)

        with_attachments = d.pop("withAttachments", UNSET)

        sharinggroup = cast(list[str], d.pop("sharinggroup", UNSET))

        metadata = d.pop("metadata", UNSET)

        uuid = d.pop("uuid", UNSET)

        publish_timestamp = d.pop("publish_timestamp", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        published = d.pop("published", UNSET)

        enforce_warninglist = d.pop("enforceWarninglist", UNSET)

        sg_reference_only = d.pop("sgReferenceOnly", UNSET)

        requested_attributes = cast(list[str], d.pop("requested_attributes", UNSET))

        include_context = d.pop("includeContext", UNSET)

        headerless = d.pop("headerless", UNSET)

        include_warninglist_hits = d.pop("includeWarninglistHits", UNSET)

        attack_galaxy = d.pop("attackGalaxy", UNSET)

        to_ids = d.pop("to_ids", UNSET)

        deleted = d.pop("deleted", UNSET)

        exclude_local_tags = d.pop("excludeLocalTags", UNSET)

        date = d.pop("date", UNSET)

        include_sightingdb = d.pop("includeSightingdb", UNSET)

        tag = d.pop("tag", UNSET)

        object_relation = d.pop("object_relation", UNSET)

        threat_level_id = d.pop("threat_level_id", UNSET)

        search_events_body = cls(
            return_format=return_format,
            page=page,
            limit=limit,
            value=value,
            type_=type_,
            category=category,
            org=org,
            tags=tags,
            event_tags=event_tags,
            searchall=searchall,
            from_=from_,
            to=to,
            last=last,
            eventid=eventid,
            with_attachments=with_attachments,
            sharinggroup=sharinggroup,
            metadata=metadata,
            uuid=uuid,
            publish_timestamp=publish_timestamp,
            timestamp=timestamp,
            published=published,
            enforce_warninglist=enforce_warninglist,
            sg_reference_only=sg_reference_only,
            requested_attributes=requested_attributes,
            include_context=include_context,
            headerless=headerless,
            include_warninglist_hits=include_warninglist_hits,
            attack_galaxy=attack_galaxy,
            to_ids=to_ids,
            deleted=deleted,
            exclude_local_tags=exclude_local_tags,
            date=date,
            include_sightingdb=include_sightingdb,
            tag=tag,
            object_relation=object_relation,
            threat_level_id=threat_level_id,
        )

        search_events_body.additional_properties = d
        return search_events_body

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
