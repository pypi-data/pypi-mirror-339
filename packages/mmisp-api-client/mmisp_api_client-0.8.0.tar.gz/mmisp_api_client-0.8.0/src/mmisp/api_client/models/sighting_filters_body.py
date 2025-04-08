from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SightingFiltersBody")


@_attrs_define
class SightingFiltersBody:
    """
    Attributes:
        value1 (Union[Unset, str]):
        value2 (Union[Unset, str]):
        type_ (Union[Unset, str]):
        category (Union[Unset, str]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        last (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        event_id (Union[Unset, int]):
        uuid (Union[Unset, str]):
        attribute_timestamp (Union[Unset, str]):
        to_ids (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        event_timestamp (Union[Unset, str]):
        eventinfo (Union[Unset, str]):
        sharinggroup (Union[Unset, list[str]]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        requested_attributes (Union[Unset, list[str]]):
        return_format (Union[Unset, str]):  Default: 'json'.
        limit (Union[Unset, str]):  Default: '25'.
    """

    value1: Union[Unset, str] = UNSET
    value2: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    last: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    event_id: Union[Unset, int] = UNSET
    uuid: Union[Unset, str] = UNSET
    attribute_timestamp: Union[Unset, str] = UNSET
    to_ids: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    event_timestamp: Union[Unset, str] = UNSET
    eventinfo: Union[Unset, str] = UNSET
    sharinggroup: Union[Unset, list[str]] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    requested_attributes: Union[Unset, list[str]] = UNSET
    return_format: Union[Unset, str] = "json"
    limit: Union[Unset, str] = "25"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value1 = self.value1

        value2 = self.value2

        type_ = self.type_

        category = self.category

        from_ = self.from_

        to = self.to

        last = self.last

        timestamp = self.timestamp

        event_id = self.event_id

        uuid = self.uuid

        attribute_timestamp = self.attribute_timestamp

        to_ids = self.to_ids

        deleted = self.deleted

        event_timestamp = self.event_timestamp

        eventinfo = self.eventinfo

        sharinggroup: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sharinggroup, Unset):
            sharinggroup = self.sharinggroup

        first_seen = self.first_seen

        last_seen = self.last_seen

        requested_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.requested_attributes, Unset):
            requested_attributes = self.requested_attributes

        return_format = self.return_format

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value1 is not UNSET:
            field_dict["value1"] = value1
        if value2 is not UNSET:
            field_dict["value2"] = value2
        if type_ is not UNSET:
            field_dict["type"] = type_
        if category is not UNSET:
            field_dict["category"] = category
        if from_ is not UNSET:
            field_dict["from_"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if last is not UNSET:
            field_dict["last"] = last
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if attribute_timestamp is not UNSET:
            field_dict["attribute_timestamp"] = attribute_timestamp
        if to_ids is not UNSET:
            field_dict["to_ids"] = to_ids
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if event_timestamp is not UNSET:
            field_dict["event_timestamp"] = event_timestamp
        if eventinfo is not UNSET:
            field_dict["eventinfo"] = eventinfo
        if sharinggroup is not UNSET:
            field_dict["sharinggroup"] = sharinggroup
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if requested_attributes is not UNSET:
            field_dict["requested_attributes"] = requested_attributes
        if return_format is not UNSET:
            field_dict["returnFormat"] = return_format
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value1 = d.pop("value1", UNSET)

        value2 = d.pop("value2", UNSET)

        type_ = d.pop("type", UNSET)

        category = d.pop("category", UNSET)

        from_ = d.pop("from_", UNSET)

        to = d.pop("to", UNSET)

        last = d.pop("last", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        event_id = d.pop("event_id", UNSET)

        uuid = d.pop("uuid", UNSET)

        attribute_timestamp = d.pop("attribute_timestamp", UNSET)

        to_ids = d.pop("to_ids", UNSET)

        deleted = d.pop("deleted", UNSET)

        event_timestamp = d.pop("event_timestamp", UNSET)

        eventinfo = d.pop("eventinfo", UNSET)

        sharinggroup = cast(list[str], d.pop("sharinggroup", UNSET))

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        requested_attributes = cast(list[str], d.pop("requested_attributes", UNSET))

        return_format = d.pop("returnFormat", UNSET)

        limit = d.pop("limit", UNSET)

        sighting_filters_body = cls(
            value1=value1,
            value2=value2,
            type_=type_,
            category=category,
            from_=from_,
            to=to,
            last=last,
            timestamp=timestamp,
            event_id=event_id,
            uuid=uuid,
            attribute_timestamp=attribute_timestamp,
            to_ids=to_ids,
            deleted=deleted,
            event_timestamp=event_timestamp,
            eventinfo=eventinfo,
            sharinggroup=sharinggroup,
            first_seen=first_seen,
            last_seen=last_seen,
            requested_attributes=requested_attributes,
            return_format=return_format,
            limit=limit,
        )

        sighting_filters_body.additional_properties = d
        return sighting_filters_body

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
