from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_all_events_event_tag_tag import GetAllEventsEventTagTag


T = TypeVar("T", bound="GetAllEventsEventTag")


@_attrs_define
class GetAllEventsEventTag:
    """
    Attributes:
        id (Union[UUID, int]):
        event_id (Union[UUID, int]):
        tag_id (int):
        local (bool):
        relationship_type (Union[Unset, bool, str]):
        tag (Union[Unset, GetAllEventsEventTagTag]):
    """

    id: Union[UUID, int]
    event_id: Union[UUID, int]
    tag_id: int
    local: bool
    relationship_type: Union[Unset, bool, str] = UNSET
    tag: Union[Unset, "GetAllEventsEventTagTag"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[int, str]
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        event_id: Union[int, str]
        if isinstance(self.event_id, UUID):
            event_id = str(self.event_id)
        else:
            event_id = self.event_id

        tag_id = self.tag_id

        local = self.local

        relationship_type: Union[Unset, bool, str]
        if isinstance(self.relationship_type, Unset):
            relationship_type = UNSET
        else:
            relationship_type = self.relationship_type

        tag: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "tag_id": tag_id,
                "local": local,
            }
        )
        if relationship_type is not UNSET:
            field_dict["relationship_type"] = relationship_type
        if tag is not UNSET:
            field_dict["Tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_all_events_event_tag_tag import GetAllEventsEventTagTag

        d = dict(src_dict)

        def _parse_id(data: object) -> Union[UUID, int]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[UUID, int], data)

        id = _parse_id(d.pop("id"))

        def _parse_event_id(data: object) -> Union[UUID, int]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                event_id_type_0 = UUID(data)

                return event_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[UUID, int], data)

        event_id = _parse_event_id(d.pop("event_id"))

        tag_id = d.pop("tag_id")

        local = d.pop("local")

        def _parse_relationship_type(data: object) -> Union[Unset, bool, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, bool, str], data)

        relationship_type = _parse_relationship_type(d.pop("relationship_type", UNSET))

        _tag = d.pop("Tag", UNSET)
        tag: Union[Unset, GetAllEventsEventTagTag]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = GetAllEventsEventTagTag.from_dict(_tag)

        get_all_events_event_tag = cls(
            id=id,
            event_id=event_id,
            tag_id=tag_id,
            local=local,
            relationship_type=relationship_type,
            tag=tag,
        )

        get_all_events_event_tag.additional_properties = d
        return get_all_events_event_tag

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
