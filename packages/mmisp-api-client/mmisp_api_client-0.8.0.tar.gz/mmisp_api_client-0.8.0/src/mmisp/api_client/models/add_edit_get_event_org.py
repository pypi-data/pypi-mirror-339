from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddEditGetEventOrg")


@_attrs_define
class AddEditGetEventOrg:
    """
    Attributes:
        id (int):
        name (str):
        uuid (Union[Unset, str]):
        local (Union[Unset, bool]):
    """

    id: int
    name: str
    uuid: Union[Unset, str] = UNSET
    local: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        uuid = self.uuid

        local = self.local

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if local is not UNSET:
            field_dict["local"] = local

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        uuid = d.pop("uuid", UNSET)

        local = d.pop("local", UNSET)

        add_edit_get_event_org = cls(
            id=id,
            name=name,
            uuid=uuid,
            local=local,
        )

        add_edit_get_event_org.additional_properties = d
        return add_edit_get_event_org

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
