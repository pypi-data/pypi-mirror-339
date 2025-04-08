from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_distribution_levels import AttributeDistributionLevels
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_attribute_tag import GetAttributeTag


T = TypeVar("T", bound="GetAttributeAttributes")


@_attrs_define
class GetAttributeAttributes:
    """
    Attributes:
        id (int):
        event_id (int):
        object_id (int):
        object_relation (Union[None, str]):
        category (str):
        type_ (str):
        value (str):
        to_ids (bool):
        uuid (str):
        timestamp (str):
        distribution (AttributeDistributionLevels): An enumeration.
        sharing_group_id (int):
        first_seen (Union[None, str]):
        last_seen (Union[None, str]):
        event_uuid (str):
        comment (Union[Unset, str]):
        deleted (Union[Unset, bool]):  Default: False.
        disable_correlation (Union[Unset, bool]):  Default: False.
        data (Union[Unset, str]):
        tag (Union[Unset, list['GetAttributeTag']]):
    """

    id: int
    event_id: int
    object_id: int
    object_relation: Union[None, str]
    category: str
    type_: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: AttributeDistributionLevels
    sharing_group_id: int
    first_seen: Union[None, str]
    last_seen: Union[None, str]
    event_uuid: str
    comment: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = False
    disable_correlation: Union[Unset, bool] = False
    data: Union[Unset, str] = UNSET
    tag: Union[Unset, list["GetAttributeTag"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        object_id = self.object_id

        object_relation: Union[None, str]
        object_relation = self.object_relation

        category = self.category

        type_ = self.type_

        value = self.value

        to_ids = self.to_ids

        uuid = self.uuid

        timestamp = self.timestamp

        distribution = self.distribution.value

        sharing_group_id = self.sharing_group_id

        first_seen: Union[None, str]
        first_seen = self.first_seen

        last_seen: Union[None, str]
        last_seen = self.last_seen

        event_uuid = self.event_uuid

        comment = self.comment

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        data = self.data

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
                "event_id": event_id,
                "object_id": object_id,
                "object_relation": object_relation,
                "category": category,
                "type": type_,
                "value": value,
                "to_ids": to_ids,
                "uuid": uuid,
                "timestamp": timestamp,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "event_uuid": event_uuid,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if disable_correlation is not UNSET:
            field_dict["disable_correlation"] = disable_correlation
        if data is not UNSET:
            field_dict["data"] = data
        if tag is not UNSET:
            field_dict["Tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_attribute_tag import GetAttributeTag

        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("event_id")

        object_id = d.pop("object_id")

        def _parse_object_relation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        object_relation = _parse_object_relation(d.pop("object_relation"))

        category = d.pop("category")

        type_ = d.pop("type")

        value = d.pop("value")

        to_ids = d.pop("to_ids")

        uuid = d.pop("uuid")

        timestamp = d.pop("timestamp")

        distribution = AttributeDistributionLevels(d.pop("distribution"))

        sharing_group_id = d.pop("sharing_group_id")

        def _parse_first_seen(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        first_seen = _parse_first_seen(d.pop("first_seen"))

        def _parse_last_seen(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        last_seen = _parse_last_seen(d.pop("last_seen"))

        event_uuid = d.pop("event_uuid")

        comment = d.pop("comment", UNSET)

        deleted = d.pop("deleted", UNSET)

        disable_correlation = d.pop("disable_correlation", UNSET)

        data = d.pop("data", UNSET)

        tag = []
        _tag = d.pop("Tag", UNSET)
        for tag_item_data in _tag or []:
            tag_item = GetAttributeTag.from_dict(tag_item_data)

            tag.append(tag_item)

        get_attribute_attributes = cls(
            id=id,
            event_id=event_id,
            object_id=object_id,
            object_relation=object_relation,
            category=category,
            type_=type_,
            value=value,
            to_ids=to_ids,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            first_seen=first_seen,
            last_seen=last_seen,
            event_uuid=event_uuid,
            comment=comment,
            deleted=deleted,
            disable_correlation=disable_correlation,
            data=data,
            tag=tag,
        )

        get_attribute_attributes.additional_properties = d
        return get_attribute_attributes

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
