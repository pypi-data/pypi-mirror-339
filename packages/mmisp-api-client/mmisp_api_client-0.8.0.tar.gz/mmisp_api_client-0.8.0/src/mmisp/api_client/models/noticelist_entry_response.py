from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.data import Data


T = TypeVar("T", bound="NoticelistEntryResponse")


@_attrs_define
class NoticelistEntryResponse:
    """
    Attributes:
        id (int):
        noticelist_id (int):
        data (Data):
    """

    id: int
    noticelist_id: int
    data: "Data"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        noticelist_id = self.noticelist_id

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "noticelist_id": noticelist_id,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data import Data

        d = dict(src_dict)
        id = d.pop("id")

        noticelist_id = d.pop("noticelist_id")

        data = Data.from_dict(d.pop("data"))

        noticelist_entry_response = cls(
            id=id,
            noticelist_id=noticelist_id,
            data=data,
        )

        noticelist_entry_response.additional_properties = d
        return noticelist_entry_response

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
