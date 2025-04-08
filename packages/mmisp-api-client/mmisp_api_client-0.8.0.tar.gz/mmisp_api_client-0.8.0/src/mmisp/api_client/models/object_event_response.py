from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectEventResponse")


@_attrs_define
class ObjectEventResponse:
    """
    Attributes:
        id (Union[UUID, int]):
        info (str):
        org_id (Union[Unset, int]):
        orgc_id (Union[Unset, int]):
    """

    id: Union[UUID, int]
    info: str
    org_id: Union[Unset, int] = UNSET
    orgc_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[int, str]
        if isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        info = self.info

        org_id = self.org_id

        orgc_id = self.orgc_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "info": info,
            }
        )
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if orgc_id is not UNSET:
            field_dict["orgc_id"] = orgc_id

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

        info = d.pop("info")

        org_id = d.pop("org_id", UNSET)

        orgc_id = d.pop("orgc_id", UNSET)

        object_event_response = cls(
            id=id,
            info=info,
            org_id=org_id,
            orgc_id=orgc_id,
        )

        object_event_response.additional_properties = d
        return object_event_response

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
