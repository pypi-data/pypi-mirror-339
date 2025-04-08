from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeleteEventResponse")


@_attrs_define
class DeleteEventResponse:
    """
    Attributes:
        saved (bool):
        name (str):
        message (str):
        url (str):
        id (Union[UUID, int]):
        success (Union[Unset, bool]):
        errors (Union[Unset, str]):
    """

    saved: bool
    name: str
    message: str
    url: str
    id: Union[UUID, int]
    success: Union[Unset, bool] = UNSET
    errors: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        name = self.name

        message = self.message

        url = self.url

        id: Union[int, str]
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        success = self.success

        errors = self.errors

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "saved": saved,
                "name": name,
                "message": message,
                "url": url,
                "id": id,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saved = d.pop("saved")

        name = d.pop("name")

        message = d.pop("message")

        url = d.pop("url")

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

        success = d.pop("success", UNSET)

        errors = d.pop("errors", UNSET)

        delete_event_response = cls(
            saved=saved,
            name=name,
            message=message,
            url=url,
            id=id,
            success=success,
            errors=errors,
        )

        delete_event_response.additional_properties = d
        return delete_event_response

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
