from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_distribution_levels import AttributeDistributionLevels
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_attribute_tag import GetAttributeTag
    from ..models.search_attributes_event import SearchAttributesEvent
    from ..models.search_attributes_object import SearchAttributesObject


T = TypeVar("T", bound="SearchAttributesAttributesDetails")


@_attrs_define
class SearchAttributesAttributesDetails:
    """
    Attributes:
        id (int):
        category (str):
        type_ (str):
        value (str):
        to_ids (bool):
        uuid (str):
        timestamp (str):
        distribution (AttributeDistributionLevels): An enumeration.
        deleted (bool):
        disable_correlation (bool):
        event_id (Union[Unset, int]):
        object_id (Union[Unset, int]):
        object_relation (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        comment (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        event_uuid (Union[Unset, str]):
        data (Union[Unset, str]):
        event (Union[Unset, SearchAttributesEvent]):
        object_ (Union[Unset, SearchAttributesObject]):
        tag (Union[Unset, list['GetAttributeTag']]):
    """

    id: int
    category: str
    type_: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: AttributeDistributionLevels
    deleted: bool
    disable_correlation: bool
    event_id: Union[Unset, int] = UNSET
    object_id: Union[Unset, int] = UNSET
    object_relation: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    event_uuid: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    event: Union[Unset, "SearchAttributesEvent"] = UNSET
    object_: Union[Unset, "SearchAttributesObject"] = UNSET
    tag: Union[Unset, list["GetAttributeTag"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        category = self.category

        type_ = self.type_

        value = self.value

        to_ids = self.to_ids

        uuid = self.uuid

        timestamp = self.timestamp

        distribution = self.distribution.value

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        event_id = self.event_id

        object_id = self.object_id

        object_relation = self.object_relation

        sharing_group_id = self.sharing_group_id

        comment = self.comment

        first_seen = self.first_seen

        last_seen = self.last_seen

        event_uuid = self.event_uuid

        data = self.data

        event: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.event, Unset):
            event = self.event.to_dict()

        object_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()

        tag: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = []
            for tag_item_data in self.tag:
                tag_item = tag_item_data.to_dict()
                tag.append(tag_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "category": category,
                "type": type_,
                "value": value,
                "to_ids": to_ids,
                "uuid": uuid,
                "timestamp": timestamp,
                "distribution": distribution,
                "deleted": deleted,
                "disable_correlation": disable_correlation,
            }
        )
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if event_uuid is not UNSET:
            field_dict["event_uuid"] = event_uuid
        if data is not UNSET:
            field_dict["data"] = data
        if event is not UNSET:
            field_dict["Event"] = event
        if object_ is not UNSET:
            field_dict["Object"] = object_
        if tag is not UNSET:
            field_dict["Tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_attribute_tag import GetAttributeTag
        from ..models.search_attributes_event import SearchAttributesEvent
        from ..models.search_attributes_object import SearchAttributesObject

        d = dict(src_dict)
        id = d.pop("id")

        category = d.pop("category")

        type_ = d.pop("type")

        value = d.pop("value")

        to_ids = d.pop("to_ids")

        uuid = d.pop("uuid")

        timestamp = d.pop("timestamp")

        distribution = AttributeDistributionLevels(d.pop("distribution"))

        deleted = d.pop("deleted")

        disable_correlation = d.pop("disable_correlation")

        event_id = d.pop("event_id", UNSET)

        object_id = d.pop("object_id", UNSET)

        object_relation = d.pop("object_relation", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        comment = d.pop("comment", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        event_uuid = d.pop("event_uuid", UNSET)

        data = d.pop("data", UNSET)

        _event = d.pop("Event", UNSET)
        event: Union[Unset, SearchAttributesEvent]
        if isinstance(_event, Unset):
            event = UNSET
        else:
            event = SearchAttributesEvent.from_dict(_event)

        _object_ = d.pop("Object", UNSET)
        object_: Union[Unset, SearchAttributesObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = SearchAttributesObject.from_dict(_object_)

        tag = []
        _tag = d.pop("Tag", UNSET)
        for tag_item_data in _tag or []:
            tag_item = GetAttributeTag.from_dict(tag_item_data)

            tag.append(tag_item)

        search_attributes_attributes_details = cls(
            id=id,
            category=category,
            type_=type_,
            value=value,
            to_ids=to_ids,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            deleted=deleted,
            disable_correlation=disable_correlation,
            event_id=event_id,
            object_id=object_id,
            object_relation=object_relation,
            sharing_group_id=sharing_group_id,
            comment=comment,
            first_seen=first_seen,
            last_seen=last_seen,
            event_uuid=event_uuid,
            data=data,
            event=event,
            object_=object_,
            tag=tag,
        )

        search_attributes_attributes_details.additional_properties = d
        return search_attributes_attributes_details

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
