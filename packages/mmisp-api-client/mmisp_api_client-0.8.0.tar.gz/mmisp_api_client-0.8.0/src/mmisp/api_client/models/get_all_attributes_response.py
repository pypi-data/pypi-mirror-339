from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.attribute_distribution_levels import AttributeDistributionLevels
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAllAttributesResponse")


@_attrs_define
class GetAllAttributesResponse:
    """
    Attributes:
        id (int):
        type_ (str):
        event_id (Union[Unset, int]):
        object_id (Union[Unset, int]):
        object_relation (Union[Unset, str]):
        category (Union[Unset, str]):
        value1 (Union[Unset, str]):
        value2 (Union[Unset, str]):
        to_ids (Union[Unset, bool]):
        uuid (Union[Unset, str]):
        timestamp (Union[Unset, str]):
        distribution (Union[Unset, AttributeDistributionLevels]): An enumeration.
        sharing_group_id (Union[Unset, int]):
        comment (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        disable_correlation (Union[Unset, bool]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        value (Union[Unset, str]):
    """

    id: int
    type_: str
    event_id: Union[Unset, int] = UNSET
    object_id: Union[Unset, int] = UNSET
    object_relation: Union[Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    value1: Union[Unset, str] = UNSET
    value2: Union[Unset, str] = UNSET
    to_ids: Union[Unset, bool] = UNSET
    uuid: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    distribution: Union[Unset, AttributeDistributionLevels] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    disable_correlation: Union[Unset, bool] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        event_id = self.event_id

        object_id = self.object_id

        object_relation = self.object_relation

        category = self.category

        value1 = self.value1

        value2 = self.value2

        to_ids = self.to_ids

        uuid = self.uuid

        timestamp = self.timestamp

        distribution: Union[Unset, int] = UNSET
        if not isinstance(self.distribution, Unset):
            distribution = self.distribution.value

        sharing_group_id = self.sharing_group_id

        comment = self.comment

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        first_seen = self.first_seen

        last_seen = self.last_seen

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if object_id is not UNSET:
            field_dict["object_id"] = object_id
        if object_relation is not UNSET:
            field_dict["object_relation"] = object_relation
        if category is not UNSET:
            field_dict["category"] = category
        if value1 is not UNSET:
            field_dict["value1"] = value1
        if value2 is not UNSET:
            field_dict["value2"] = value2
        if to_ids is not UNSET:
            field_dict["to_ids"] = to_ids
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if comment is not UNSET:
            field_dict["comment"] = comment
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if disable_correlation is not UNSET:
            field_dict["disable_correlation"] = disable_correlation
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        event_id = d.pop("event_id", UNSET)

        object_id = d.pop("object_id", UNSET)

        object_relation = d.pop("object_relation", UNSET)

        category = d.pop("category", UNSET)

        value1 = d.pop("value1", UNSET)

        value2 = d.pop("value2", UNSET)

        to_ids = d.pop("to_ids", UNSET)

        uuid = d.pop("uuid", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        _distribution = d.pop("distribution", UNSET)
        distribution: Union[Unset, AttributeDistributionLevels]
        if isinstance(_distribution, Unset):
            distribution = UNSET
        else:
            distribution = AttributeDistributionLevels(_distribution)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        comment = d.pop("comment", UNSET)

        deleted = d.pop("deleted", UNSET)

        disable_correlation = d.pop("disable_correlation", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        value = d.pop("value", UNSET)

        get_all_attributes_response = cls(
            id=id,
            type_=type_,
            event_id=event_id,
            object_id=object_id,
            object_relation=object_relation,
            category=category,
            value1=value1,
            value2=value2,
            to_ids=to_ids,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            comment=comment,
            deleted=deleted,
            disable_correlation=disable_correlation,
            first_seen=first_seen,
            last_seen=last_seen,
            value=value,
        )

        get_all_attributes_response.additional_properties = d
        return get_all_attributes_response

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
