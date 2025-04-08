from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublishEventResponse")


@_attrs_define
class PublishEventResponse:
    """
    Attributes:
        name (str):
        message (str):
        url (str):
        saved (Union[Unset, bool]):
        success (Union[Unset, bool]):
        id (Union[UUID, Unset, int]):
    """

    name: str
    message: str
    url: str
    saved: Union[Unset, bool] = UNSET
    success: Union[Unset, bool] = UNSET
    id: Union[UUID, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        message = self.message

        url = self.url

        saved = self.saved

        success = self.success

        id: Union[Unset, int, str]
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "message": message,
                "url": url,
            }
        )
        if saved is not UNSET:
            field_dict["saved"] = saved
        if success is not UNSET:
            field_dict["success"] = success
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        message = d.pop("message")

        url = d.pop("url")

        saved = d.pop("saved", UNSET)

        success = d.pop("success", UNSET)

        def _parse_id(data: object) -> Union[UUID, Unset, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                id_type_0 = UUID(data)

                return id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[UUID, Unset, int], data)

        id = _parse_id(d.pop("id", UNSET))

        publish_event_response = cls(
            name=name,
            message=message,
            url=url,
            saved=saved,
            success=success,
            id=id,
        )

        publish_event_response.additional_properties = d
        return publish_event_response

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
