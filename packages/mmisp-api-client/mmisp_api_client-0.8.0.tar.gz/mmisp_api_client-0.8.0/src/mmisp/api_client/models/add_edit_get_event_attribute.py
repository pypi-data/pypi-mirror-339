from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_galaxy import AddEditGetEventGalaxy
    from ..models.add_edit_get_event_tag import AddEditGetEventTag
    from ..models.event_sharing_group_response import EventSharingGroupResponse


T = TypeVar("T", bound="AddEditGetEventAttribute")


@_attrs_define
class AddEditGetEventAttribute:
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
        distribution (str):
        sharing_group_id (int):
        deleted (bool):
        disable_correlation (bool):
        object_relation (Union[Unset, str]):
        comment (Union[Unset, str]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        galaxy (Union[Unset, list['AddEditGetEventGalaxy']]):
        sharing_group (Union[Unset, EventSharingGroupResponse]):
        shadow_attribute (Union[Unset, list[str]]):
        tag (Union[Unset, list['AddEditGetEventTag']]):
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
    distribution: str
    sharing_group_id: int
    deleted: bool
    disable_correlation: bool
    object_relation: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    galaxy: Union[Unset, list["AddEditGetEventGalaxy"]] = UNSET
    sharing_group: Union[Unset, "EventSharingGroupResponse"] = UNSET
    shadow_attribute: Union[Unset, list[str]] = UNSET
    tag: Union[Unset, list["AddEditGetEventTag"]] = UNSET
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

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        deleted = self.deleted

        disable_correlation = self.disable_correlation

        object_relation = self.object_relation

        comment = self.comment

        first_seen = self.first_seen

        last_seen = self.last_seen

        galaxy: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.galaxy, Unset):
            galaxy = []
            for galaxy_item_data in self.galaxy:
                galaxy_item = galaxy_item_data.to_dict()
                galaxy.append(galaxy_item)

        sharing_group: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.sharing_group, Unset):
            sharing_group = self.sharing_group.to_dict()

        shadow_attribute: Union[Unset, list[str]] = UNSET
        if not isinstance(self.shadow_attribute, Unset):
            shadow_attribute = self.shadow_attribute

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
        if galaxy is not UNSET:
            field_dict["Galaxy"] = galaxy
        if sharing_group is not UNSET:
            field_dict["SharingGroup"] = sharing_group
        if shadow_attribute is not UNSET:
            field_dict["ShadowAttribute"] = shadow_attribute
        if tag is not UNSET:
            field_dict["Tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_galaxy import AddEditGetEventGalaxy
        from ..models.add_edit_get_event_tag import AddEditGetEventTag
        from ..models.event_sharing_group_response import EventSharingGroupResponse

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

        distribution = d.pop("distribution")

        sharing_group_id = d.pop("sharing_group_id")

        deleted = d.pop("deleted")

        disable_correlation = d.pop("disable_correlation")

        object_relation = d.pop("object_relation", UNSET)

        comment = d.pop("comment", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        galaxy = []
        _galaxy = d.pop("Galaxy", UNSET)
        for galaxy_item_data in _galaxy or []:
            galaxy_item = AddEditGetEventGalaxy.from_dict(galaxy_item_data)

            galaxy.append(galaxy_item)

        _sharing_group = d.pop("SharingGroup", UNSET)
        sharing_group: Union[Unset, EventSharingGroupResponse]
        if isinstance(_sharing_group, Unset):
            sharing_group = UNSET
        else:
            sharing_group = EventSharingGroupResponse.from_dict(_sharing_group)

        shadow_attribute = cast(list[str], d.pop("ShadowAttribute", UNSET))

        tag = []
        _tag = d.pop("Tag", UNSET)
        for tag_item_data in _tag or []:
            tag_item = AddEditGetEventTag.from_dict(tag_item_data)

            tag.append(tag_item)

        add_edit_get_event_attribute = cls(
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
            object_relation=object_relation,
            comment=comment,
            first_seen=first_seen,
            last_seen=last_seen,
            galaxy=galaxy,
            sharing_group=sharing_group,
            shadow_attribute=shadow_attribute,
            tag=tag,
        )

        add_edit_get_event_attribute.additional_properties = d
        return add_edit_get_event_attribute

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
