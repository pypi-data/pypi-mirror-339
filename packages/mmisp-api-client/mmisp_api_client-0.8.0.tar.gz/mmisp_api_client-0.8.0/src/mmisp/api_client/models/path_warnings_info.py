from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PathWarningsInfo")


@_attrs_define
class PathWarningsInfo:
    """
    Attributes:
        source_id (int):
        next_node_id (int):
        warning (str):
        blocking (bool):
        module_name (str):
        module_id (int):
    """

    source_id: int
    next_node_id: int
    warning: str
    blocking: bool
    module_name: str
    module_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source_id = self.source_id

        next_node_id = self.next_node_id

        warning = self.warning

        blocking = self.blocking

        module_name = self.module_name

        module_id = self.module_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_id": source_id,
                "next_node_id": next_node_id,
                "warning": warning,
                "blocking": blocking,
                "module_name": module_name,
                "module_id": module_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_id = d.pop("source_id")

        next_node_id = d.pop("next_node_id")

        warning = d.pop("warning")

        blocking = d.pop("blocking")

        module_name = d.pop("module_name")

        module_id = d.pop("module_id")

        path_warnings_info = cls(
            source_id=source_id,
            next_node_id=next_node_id,
            warning=warning,
            blocking=blocking,
            module_name=module_name,
            module_id=module_id,
        )

        path_warnings_info.additional_properties = d
        return path_warnings_info

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
