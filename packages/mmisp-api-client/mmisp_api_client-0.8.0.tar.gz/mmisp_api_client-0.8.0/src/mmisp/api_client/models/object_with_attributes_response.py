from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_all_attributes_response import GetAllAttributesResponse
    from ..models.object_event_response import ObjectEventResponse


T = TypeVar("T", bound="ObjectWithAttributesResponse")


@_attrs_define
class ObjectWithAttributesResponse:
    """
    Attributes:
        id (int):
        uuid (str):
        name (str):
        meta_category (Union[Unset, str]):
        description (Union[Unset, str]):
        template_uuid (Union[Unset, str]):
        template_version (Union[Unset, str]):
        event_id (Union[Unset, int]):
        timestamp (Union[Unset, str]):
        distribution (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        comment (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        attribute (Union[Unset, list['GetAllAttributesResponse']]):
        event (Union[Unset, ObjectEventResponse]):
    """

    id: int
    uuid: str
    name: str
    meta_category: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    template_uuid: Union[Unset, str] = UNSET
    template_version: Union[Unset, str] = UNSET
    event_id: Union[Unset, int] = UNSET
    timestamp: Union[Unset, str] = UNSET
    distribution: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    attribute: Union[Unset, list["GetAllAttributesResponse"]] = UNSET
    event: Union[Unset, "ObjectEventResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        name = self.name

        meta_category = self.meta_category

        description = self.description

        template_uuid = self.template_uuid

        template_version = self.template_version

        event_id = self.event_id

        timestamp = self.timestamp

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        comment = self.comment

        deleted = self.deleted

        first_seen = self.first_seen

        last_seen = self.last_seen

        attribute: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attribute, Unset):
            attribute = []
            for attribute_item_data in self.attribute:
                attribute_item = attribute_item_data.to_dict()
                attribute.append(attribute_item)

        event: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.event, Unset):
            event = self.event.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "name": name,
            }
        )
        if meta_category is not UNSET:
            field_dict["meta_category"] = meta_category
        if description is not UNSET:
            field_dict["description"] = description
        if template_uuid is not UNSET:
            field_dict["template_uuid"] = template_uuid
        if template_version is not UNSET:
            field_dict["template_version"] = template_version
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
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
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if attribute is not UNSET:
            field_dict["Attribute"] = attribute
        if event is not UNSET:
            field_dict["Event"] = event

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_all_attributes_response import GetAllAttributesResponse
        from ..models.object_event_response import ObjectEventResponse

        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        name = d.pop("name")

        meta_category = d.pop("meta_category", UNSET)

        description = d.pop("description", UNSET)

        template_uuid = d.pop("template_uuid", UNSET)

        template_version = d.pop("template_version", UNSET)

        event_id = d.pop("event_id", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        distribution = d.pop("distribution", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        comment = d.pop("comment", UNSET)

        deleted = d.pop("deleted", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        attribute = []
        _attribute = d.pop("Attribute", UNSET)
        for attribute_item_data in _attribute or []:
            attribute_item = GetAllAttributesResponse.from_dict(attribute_item_data)

            attribute.append(attribute_item)

        _event = d.pop("Event", UNSET)
        event: Union[Unset, ObjectEventResponse]
        if isinstance(_event, Unset):
            event = UNSET
        else:
            event = ObjectEventResponse.from_dict(_event)

        object_with_attributes_response = cls(
            id=id,
            uuid=uuid,
            name=name,
            meta_category=meta_category,
            description=description,
            template_uuid=template_uuid,
            template_version=template_version,
            event_id=event_id,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            comment=comment,
            deleted=deleted,
            first_seen=first_seen,
            last_seen=last_seen,
            attribute=attribute,
            event=event,
        )

        object_with_attributes_response.additional_properties = d
        return object_with_attributes_response

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
