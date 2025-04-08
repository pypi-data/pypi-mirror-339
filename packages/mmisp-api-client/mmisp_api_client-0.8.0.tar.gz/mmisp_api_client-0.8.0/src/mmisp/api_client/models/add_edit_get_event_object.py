from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_attribute import AddEditGetEventAttribute


T = TypeVar("T", bound="AddEditGetEventObject")


@_attrs_define
class AddEditGetEventObject:
    """
    Attributes:
        id (int):
        name (str):
        meta_category (str):
        description (str):
        template_uuid (str):
        template_version (str):
        event_id (int):
        uuid (str):
        timestamp (str):
        distribution (str):
        sharing_group_id (int):
        comment (str):
        deleted (bool):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        object_reference (Union[Unset, list[str]]):
        attribute (Union[Unset, list['AddEditGetEventAttribute']]):
    """

    id: int
    name: str
    meta_category: str
    description: str
    template_uuid: str
    template_version: str
    event_id: int
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: int
    comment: str
    deleted: bool
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    object_reference: Union[Unset, list[str]] = UNSET
    attribute: Union[Unset, list["AddEditGetEventAttribute"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        meta_category = self.meta_category

        description = self.description

        template_uuid = self.template_uuid

        template_version = self.template_version

        event_id = self.event_id

        uuid = self.uuid

        timestamp = self.timestamp

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        comment = self.comment

        deleted = self.deleted

        first_seen = self.first_seen

        last_seen = self.last_seen

        object_reference: Union[Unset, list[str]] = UNSET
        if not isinstance(self.object_reference, Unset):
            object_reference = self.object_reference

        attribute: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attribute, Unset):
            attribute = []
            for attribute_item_data in self.attribute:
                attribute_item = attribute_item_data.to_dict()
                attribute.append(attribute_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "meta_category": meta_category,
                "description": description,
                "template_uuid": template_uuid,
                "template_version": template_version,
                "event_id": event_id,
                "uuid": uuid,
                "timestamp": timestamp,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "comment": comment,
                "deleted": deleted,
            }
        )
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if object_reference is not UNSET:
            field_dict["ObjectReference"] = object_reference
        if attribute is not UNSET:
            field_dict["Attribute"] = attribute

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_attribute import AddEditGetEventAttribute

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        meta_category = d.pop("meta_category")

        description = d.pop("description")

        template_uuid = d.pop("template_uuid")

        template_version = d.pop("template_version")

        event_id = d.pop("event_id")

        uuid = d.pop("uuid")

        timestamp = d.pop("timestamp")

        distribution = d.pop("distribution")

        sharing_group_id = d.pop("sharing_group_id")

        comment = d.pop("comment")

        deleted = d.pop("deleted")

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        object_reference = cast(list[str], d.pop("ObjectReference", UNSET))

        attribute = []
        _attribute = d.pop("Attribute", UNSET)
        for attribute_item_data in _attribute or []:
            attribute_item = AddEditGetEventAttribute.from_dict(attribute_item_data)

            attribute.append(attribute_item)

        add_edit_get_event_object = cls(
            id=id,
            name=name,
            meta_category=meta_category,
            description=description,
            template_uuid=template_uuid,
            template_version=template_version,
            event_id=event_id,
            uuid=uuid,
            timestamp=timestamp,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            comment=comment,
            deleted=deleted,
            first_seen=first_seen,
            last_seen=last_seen,
            object_reference=object_reference,
            attribute=attribute,
        )

        add_edit_get_event_object.additional_properties = d
        return add_edit_get_event_object

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
