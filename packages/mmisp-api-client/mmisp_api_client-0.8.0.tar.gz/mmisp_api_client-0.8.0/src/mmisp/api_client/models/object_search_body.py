from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectSearchBody")


@_attrs_define
class ObjectSearchBody:
    """
    Attributes:
        object_name (Union[Unset, str]):
        object_template_uuid (Union[Unset, str]):
        object_template_version (Union[Unset, str]):
        event_id (Union[Unset, int]):
        category (Union[Unset, str]):
        comment (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        quick_filter (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        event_info (Union[Unset, str]):
        from_ (Union[Unset, str]):
        to (Union[Unset, str]):
        date (Union[Unset, str]):
        last (Union[Unset, str]):
        event_timestamp (Union[Unset, str]):
        org_id (Union[Unset, int]):
        uuid (Union[Unset, str]):
        value1 (Union[Unset, str]):
        value2 (Union[Unset, str]):
        type_ (Union[Unset, str]):
        object_relation (Union[Unset, str]):
        attribute_timestamp (Union[Unset, str]):
        to_ids (Union[Unset, bool]):
        published (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        return_format (Union[Unset, str]):  Default: 'json'.
        limit (Union[Unset, str]):  Default: '25'.
    """

    object_name: Union[Unset, str] = UNSET
    object_template_uuid: Union[Unset, str] = UNSET
    object_template_version: Union[Unset, str] = UNSET
    event_id: Union[Unset, int] = UNSET
    category: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    quick_filter: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    event_info: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    date: Union[Unset, str] = UNSET
    last: Union[Unset, str] = UNSET
    event_timestamp: Union[Unset, str] = UNSET
    org_id: Union[Unset, int] = UNSET
    uuid: Union[Unset, str] = UNSET
    value1: Union[Unset, str] = UNSET
    value2: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    object_relation: Union[Unset, str] = UNSET
    attribute_timestamp: Union[Unset, str] = UNSET
    to_ids: Union[Unset, bool] = UNSET
    published: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    return_format: Union[Unset, str] = "json"
    limit: Union[Unset, str] = "25"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_name = self.object_name

        object_template_uuid = self.object_template_uuid

        object_template_version = self.object_template_version

        event_id = self.event_id

        category = self.category

        comment = self.comment

        first_seen = self.first_seen

        last_seen = self.last_seen

        quick_filter = self.quick_filter

        timestamp = self.timestamp

        event_info = self.event_info

        from_ = self.from_

        to = self.to

        date = self.date

        last = self.last

        event_timestamp = self.event_timestamp

        org_id = self.org_id

        uuid = self.uuid

        value1 = self.value1

        value2 = self.value2

        type_ = self.type_

        object_relation = self.object_relation

        attribute_timestamp = self.attribute_timestamp

        to_ids = self.to_ids

        published = self.published

        deleted = self.deleted

        return_format = self.return_format

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_name is not UNSET:
            field_dict["object_name"] = object_name
        if object_template_uuid is not UNSET:
            field_dict["object_template_uuid"] = object_template_uuid
        if object_template_version is not UNSET:
            field_dict["object_template_version"] = object_template_version
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if category is not UNSET:
            field_dict["category"] = category
        if comment is not UNSET:
            field_dict["comment"] = comment
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if quick_filter is not UNSET:
            field_dict["quick_filter"] = quick_filter
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if event_info is not UNSET:
            field_dict["event_info"] = event_info
        if from_ is not UNSET:
            field_dict["from_"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if date is not UNSET:
            field_dict["date"] = date
        if last is not UNSET:
            field_dict["last"] = last
        if event_timestamp is not UNSET:
            field_dict["event_timestamp"] = event_timestamp
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if value1 is not UNSET:
            field_dict["value1"] = value1
        if value2 is not UNSET:
            field_dict["value2"] = value2
        if type_ is not UNSET:
            field_dict["type"] = type_
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if attribute_timestamp is not UNSET:
            field_dict["attribute_timestamp"] = attribute_timestamp
        if to_ids is not UNSET:
            field_dict["to_ids"] = to_ids
        if published is not UNSET:
            field_dict["published"] = published
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if return_format is not UNSET:
            field_dict["return_format"] = return_format
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_name = d.pop("object_name", UNSET)

        object_template_uuid = d.pop("object_template_uuid", UNSET)

        object_template_version = d.pop("object_template_version", UNSET)

        event_id = d.pop("event_id", UNSET)

        category = d.pop("category", UNSET)

        comment = d.pop("comment", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        quick_filter = d.pop("quick_filter", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        event_info = d.pop("event_info", UNSET)

        from_ = d.pop("from_", UNSET)

        to = d.pop("to", UNSET)

        date = d.pop("date", UNSET)

        last = d.pop("last", UNSET)

        event_timestamp = d.pop("event_timestamp", UNSET)

        org_id = d.pop("org_id", UNSET)

        uuid = d.pop("uuid", UNSET)

        value1 = d.pop("value1", UNSET)

        value2 = d.pop("value2", UNSET)

        type_ = d.pop("type", UNSET)

        object_relation = d.pop("object_relation", UNSET)

        attribute_timestamp = d.pop("attribute_timestamp", UNSET)

        to_ids = d.pop("to_ids", UNSET)

        published = d.pop("published", UNSET)

        deleted = d.pop("deleted", UNSET)

        return_format = d.pop("return_format", UNSET)

        limit = d.pop("limit", UNSET)

        object_search_body = cls(
            object_name=object_name,
            object_template_uuid=object_template_uuid,
            object_template_version=object_template_version,
            event_id=event_id,
            category=category,
            comment=comment,
            first_seen=first_seen,
            last_seen=last_seen,
            quick_filter=quick_filter,
            timestamp=timestamp,
            event_info=event_info,
            from_=from_,
            to=to,
            date=date,
            last=last,
            event_timestamp=event_timestamp,
            org_id=org_id,
            uuid=uuid,
            value1=value1,
            value2=value2,
            type_=type_,
            object_relation=object_relation,
            attribute_timestamp=attribute_timestamp,
            to_ids=to_ids,
            published=published,
            deleted=deleted,
            return_format=return_format,
            limit=limit,
        )

        object_search_body.additional_properties = d
        return object_search_body

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
