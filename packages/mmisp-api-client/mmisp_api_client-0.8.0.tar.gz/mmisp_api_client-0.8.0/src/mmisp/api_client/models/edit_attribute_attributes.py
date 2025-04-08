from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_distribution_levels import AttributeDistributionLevels
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_attribute_tag import EditAttributeTag


T = TypeVar("T", bound="EditAttributeAttributes")


@_attrs_define
class EditAttributeAttributes:
    """
    Attributes:
        id (int):
        event_id (int):
        object_id (int):
        category (str):
        type_ (str):
        value (str):
        to_ids (bool):
        uuid (str):
        timestamp (str):
        distribution (AttributeDistributionLevels): An enumeration.
        sharing_group_id (int):
        deleted (bool):
        disable_correlation (bool):
        tag (list['EditAttributeTag']):
        object_relation (Union[Unset, str]):
        comment (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
    """

    id: int
    event_id: int
    object_id: int
    category: str
    type_: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: AttributeDistributionLevels
    sharing_group_id: int
    deleted: bool
    disable_correlation: bool
    tag: list["EditAttributeTag"]
    object_relation: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        object_id = self.object_id

        category = self.category

        type_ = self.type_

        value = self.value

        to_ids = self.to_ids

        uuid = self.uuid

        timestamp = self.timestamp

        distribution = self.distribution.value

        sharing_group_id = self.sharing_group_id

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        tag = []
        for tag_item_data in self.tag:
            tag_item = tag_item_data.to_dict()
            tag.append(tag_item)

        object_relation = self.object_relation

        comment = self.comment

        first_seen = self.first_seen

        last_seen = self.last_seen

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "object_id": object_id,
                "category": category,
                "type": type_,
                "value": value,
                "to_ids": to_ids,
                "uuid": uuid,
                "timestamp": timestamp,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "deleted": deleted,
                "disable_correlation": disable_correlation,
                "Tag": tag,
            }
        )
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if comment is not UNSET:
            field_dict["comment"] = comment
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.edit_attribute_tag import EditAttributeTag

        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("event_id")

        object_id = d.pop("object_id")

        category = d.pop("category")

        type_ = d.pop("type")

        value = d.pop("value")

        to_ids = d.pop("to_ids")

        uuid = d.pop("uuid")

        timestamp = d.pop("timestamp")

        distribution = AttributeDistributionLevels(d.pop("distribution"))

        sharing_group_id = d.pop("sharing_group_id")

        deleted = d.pop("deleted")

        disable_correlation = d.pop("disable_correlation")

        tag = []
        _tag = d.pop("Tag")
        for tag_item_data in _tag:
            tag_item = EditAttributeTag.from_dict(tag_item_data)

            tag.append(tag_item)

        object_relation = d.pop("object_relation", UNSET)

        comment = d.pop("comment", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        edit_attribute_attributes = cls(
            id=id,
            event_id=event_id,
            object_id=object_id,
            category=category,
            type_=type_,
            value=value,
            to_ids=to_ids,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            deleted=deleted,
            disable_correlation=disable_correlation,
            tag=tag,
            object_relation=object_relation,
            comment=comment,
            first_seen=first_seen,
            last_seen=last_seen,
        )

        edit_attribute_attributes.additional_properties = d
        return edit_attribute_attributes

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
