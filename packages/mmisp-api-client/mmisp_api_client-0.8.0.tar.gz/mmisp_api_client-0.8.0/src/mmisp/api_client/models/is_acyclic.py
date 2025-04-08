from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.is_acyclic_info import IsAcyclicInfo


T = TypeVar("T", bound="IsAcyclic")


@_attrs_define
class IsAcyclic:
    """Represents the whether graph is acyclic and details of the first detected cycle.

    - **is_acyclic**: False if the graph contains at least one cycle.
    - **cycles**: A list of entries, each containing two node IDs and a "Cycle" string.
    Conbined they result in the cycle.

    Example:
    ```json
    "is_acyclic": {
        "is_acyclic": false,
        "cycles": [
            [
                4,
                3,
                "Cycle"
            ],
            [
                3,
                4,
                "Cycle"
            ]
        ]
    }
    ```

        Attributes:
            is_acyclic (bool):
            cycles (list['IsAcyclicInfo']):
    """

    is_acyclic: bool
    cycles: list["IsAcyclicInfo"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_acyclic = self.is_acyclic

        cycles = []
        for cycles_item_data in self.cycles:
            cycles_item = cycles_item_data.to_dict()
            cycles.append(cycles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_acyclic": is_acyclic,
                "cycles": cycles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.is_acyclic_info import IsAcyclicInfo

        d = dict(src_dict)
        is_acyclic = d.pop("is_acyclic")

        cycles = []
        _cycles = d.pop("cycles")
        for cycles_item_data in _cycles:
            cycles_item = IsAcyclicInfo.from_dict(cycles_item_data)

            cycles.append(cycles_item)

        is_acyclic = cls(
            is_acyclic=is_acyclic,
            cycles=cycles,
        )

        is_acyclic.additional_properties = d
        return is_acyclic

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
