from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="IsAcyclicInfo")


@_attrs_define
class IsAcyclicInfo:
    """
    Attributes:
        node_id1 (int):
        node_id2 (int):
        cycle (Union[Unset, str]):  Default: 'Cycle'.
    """

    node_id1: int
    node_id2: int
    cycle: Union[Unset, str] = "Cycle"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        node_id1 = self.node_id1

        node_id2 = self.node_id2

        cycle = self.cycle

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nodeID1": node_id1,
                "nodeID2": node_id2,
            }
        )
        if cycle is not UNSET:
            field_dict["cycle"] = cycle

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        node_id1 = d.pop("nodeID1")

        node_id2 = d.pop("nodeID2")

        cycle = d.pop("cycle", UNSET)

        is_acyclic_info = cls(
            node_id1=node_id1,
            node_id2=node_id2,
            cycle=cycle,
        )

        is_acyclic_info.additional_properties = d
        return is_acyclic_info

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
