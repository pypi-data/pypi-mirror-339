from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IndexEventsBody")


@_attrs_define
class IndexEventsBody:
    """
    Attributes:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        sort (Union[Unset, int]):
        direction (Union[Unset, int]):
        minimal (Union[Unset, bool]):
        attribute (Union[Unset, str]):
        eventid (Union[Unset, int]):
        datefrom (Union[Unset, str]):
        dateuntil (Union[Unset, str]):
        org (Union[Unset, str]):
        eventinfo (Union[Unset, str]):
        tag (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        distribution (Union[Unset, str]):
        sharinggroup (Union[Unset, str]):
        analysis (Union[Unset, str]):
        threatlevel (Union[Unset, str]):
        email (Union[Unset, str]):
        hasproposal (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        publish_timestamp (Union[Unset, str]):
        search_datefrom (Union[Unset, str]):
        search_dateuntil (Union[Unset, str]):
    """

    page: Union[Unset, int] = UNSET
    limit: Union[Unset, int] = UNSET
    sort: Union[Unset, int] = UNSET
    direction: Union[Unset, int] = UNSET
    minimal: Union[Unset, bool] = UNSET
    attribute: Union[Unset, str] = UNSET
    eventid: Union[Unset, int] = UNSET
    datefrom: Union[Unset, str] = UNSET
    dateuntil: Union[Unset, str] = UNSET
    org: Union[Unset, str] = UNSET
    eventinfo: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    distribution: Union[Unset, str] = UNSET
    sharinggroup: Union[Unset, str] = UNSET
    analysis: Union[Unset, str] = UNSET
    threatlevel: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    hasproposal: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    publish_timestamp: Union[Unset, str] = UNSET
    search_datefrom: Union[Unset, str] = UNSET
    search_dateuntil: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        limit = self.limit

        sort = self.sort

        direction = self.direction

        minimal = self.minimal

        attribute = self.attribute

        eventid = self.eventid

        datefrom = self.datefrom

        dateuntil = self.dateuntil

        org = self.org

        eventinfo = self.eventinfo

        tag = self.tag

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        distribution = self.distribution

        sharinggroup = self.sharinggroup

        analysis = self.analysis

        threatlevel = self.threatlevel

        email = self.email

        hasproposal = self.hasproposal

        timestamp = self.timestamp

        publish_timestamp = self.publish_timestamp

        search_datefrom = self.search_datefrom

        search_dateuntil = self.search_dateuntil

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit
        if sort is not UNSET:
            field_dict["sort"] = sort
        if direction is not UNSET:
            field_dict["direction"] = direction
        if minimal is not UNSET:
            field_dict["minimal"] = minimal
        if attribute is not UNSET:
            field_dict["attribute"] = attribute
        if eventid is not UNSET:
            field_dict["eventid"] = eventid
        if datefrom is not UNSET:
            field_dict["datefrom"] = datefrom
        if dateuntil is not UNSET:
            field_dict["dateuntil"] = dateuntil
        if org is not UNSET:
            field_dict["org"] = org
        if eventinfo is not UNSET:
            field_dict["eventinfo"] = eventinfo
        if tag is not UNSET:
            field_dict["tag"] = tag
        if tags is not UNSET:
            field_dict["tags"] = tags
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if sharinggroup is not UNSET:
            field_dict["sharinggroup"] = sharinggroup
        if analysis is not UNSET:
            field_dict["analysis"] = analysis
        if threatlevel is not UNSET:
            field_dict["threatlevel"] = threatlevel
        if email is not UNSET:
            field_dict["email"] = email
        if hasproposal is not UNSET:
            field_dict["hasproposal"] = hasproposal
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if publish_timestamp is not UNSET:
            field_dict["publish_timestamp"] = publish_timestamp
        if search_datefrom is not UNSET:
            field_dict["searchDatefrom"] = search_datefrom
        if search_dateuntil is not UNSET:
            field_dict["searchDateuntil"] = search_dateuntil

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        sort = d.pop("sort", UNSET)

        direction = d.pop("direction", UNSET)

        minimal = d.pop("minimal", UNSET)

        attribute = d.pop("attribute", UNSET)

        eventid = d.pop("eventid", UNSET)

        datefrom = d.pop("datefrom", UNSET)

        dateuntil = d.pop("dateuntil", UNSET)

        org = d.pop("org", UNSET)

        eventinfo = d.pop("eventinfo", UNSET)

        tag = d.pop("tag", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        distribution = d.pop("distribution", UNSET)

        sharinggroup = d.pop("sharinggroup", UNSET)

        analysis = d.pop("analysis", UNSET)

        threatlevel = d.pop("threatlevel", UNSET)

        email = d.pop("email", UNSET)

        hasproposal = d.pop("hasproposal", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        publish_timestamp = d.pop("publish_timestamp", UNSET)

        search_datefrom = d.pop("searchDatefrom", UNSET)

        search_dateuntil = d.pop("searchDateuntil", UNSET)

        index_events_body = cls(
            page=page,
            limit=limit,
            sort=sort,
            direction=direction,
            minimal=minimal,
            attribute=attribute,
            eventid=eventid,
            datefrom=datefrom,
            dateuntil=dateuntil,
            org=org,
            eventinfo=eventinfo,
            tag=tag,
            tags=tags,
            distribution=distribution,
            sharinggroup=sharinggroup,
            analysis=analysis,
            threatlevel=threatlevel,
            email=email,
            hasproposal=hasproposal,
            timestamp=timestamp,
            publish_timestamp=publish_timestamp,
            search_datefrom=search_datefrom,
            search_dateuntil=search_dateuntil,
        )

        index_events_body.additional_properties = d
        return index_events_body

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
