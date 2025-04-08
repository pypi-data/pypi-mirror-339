from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_distribution_levels import AttributeDistributionLevels
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddAttributeAttributes")


@_attrs_define
class AddAttributeAttributes:
    """
    Attributes:
        id (int):
        event_id (int):
        object_id (int):
        object_relation (Union[None, str]):
        category (str):
        type_ (str):
        value (str):
        value1 (str):
        value2 (str):
        to_ids (bool):
        uuid (str):
        timestamp (str):
        distribution (AttributeDistributionLevels): An enumeration.
        sharing_group_id (int):
        deleted (bool):
        disable_correlation (bool):
        comment (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        attribute_tag (Union[Unset, list[str]]):
    """

    id: int
    event_id: int
    object_id: int
    object_relation: Union[None, str]
    category: str
    type_: str
    value: str
    value1: str
    value2: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: AttributeDistributionLevels
    sharing_group_id: int
    deleted: bool
    disable_correlation: bool
    comment: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    attribute_tag: Union[Unset, list[str]] = UNSET
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

        value1 = self.value1

        value2 = self.value2

        to_ids = self.to_ids

        uuid = self.uuid

        timestamp = self.timestamp

        distribution = self.distribution.value

        sharing_group_id = self.sharing_group_id

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        comment = self.comment

        first_seen = self.first_seen

        last_seen = self.last_seen

        attribute_tag: Union[Unset, list[str]] = UNSET
        if not isinstance(self.attribute_tag, Unset):
            attribute_tag = self.attribute_tag

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
                "value1": value1,
                "value2": value2,
                "to_ids": to_ids,
                "uuid": uuid,
                "timestamp": timestamp,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "deleted": deleted,
                "disable_correlation": disable_correlation,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if attribute_tag is not UNSET:
            field_dict["AttributeTag"] = attribute_tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        value1 = d.pop("value1")

        value2 = d.pop("value2")

        to_ids = d.pop("to_ids")

        uuid = d.pop("uuid")

        timestamp = d.pop("timestamp")

        distribution = AttributeDistributionLevels(d.pop("distribution"))

        sharing_group_id = d.pop("sharing_group_id")

        deleted = d.pop("deleted")

        disable_correlation = d.pop("disable_correlation")

        comment = d.pop("comment", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        attribute_tag = cast(list[str], d.pop("AttributeTag", UNSET))

        add_attribute_attributes = cls(
            id=id,
            event_id=event_id,
            object_id=object_id,
            object_relation=object_relation,
            category=category,
            type_=type_,
            value=value,
            value1=value1,
            value2=value2,
            to_ids=to_ids,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            deleted=deleted,
            disable_correlation=disable_correlation,
            comment=comment,
            first_seen=first_seen,
            last_seen=last_seen,
            attribute_tag=attribute_tag,
        )

        add_attribute_attributes.additional_properties = d
        return add_attribute_attributes

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
