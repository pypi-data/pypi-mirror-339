from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetAllEventsEventTagTag")


@_attrs_define
class GetAllEventsEventTagTag:
    """
    Attributes:
        id (Union[UUID, int]):
        name (str):
        colour (str):
        is_galaxy (bool):
    """

    id: Union[UUID, int]
    name: str
    colour: str
    is_galaxy: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[int, str]
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        name = self.name

        colour = self.colour

        is_galaxy = self.is_galaxy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "colour": colour,
                "is_galaxy": is_galaxy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        name = d.pop("name")

        colour = d.pop("colour")

        is_galaxy = d.pop("is_galaxy")

        get_all_events_event_tag_tag = cls(
            id=id,
            name=name,
            colour=colour,
            is_galaxy=is_galaxy,
        )

        get_all_events_event_tag_tag.additional_properties = d
        return get_all_events_event_tag_tag

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
