from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.path_warnings_info import PathWarningsInfo


T = TypeVar("T", bound="PathWarnings")


@_attrs_define
class PathWarnings:
    """Represents warnings for paths in a graph.

    - **has_path_warnings**: True if the graph contains at least one warning.
    - **edges**: A list containing all connections which are flagged as warnings.

    Example:
    ```json
    "path_warnings": {
        "has_path_warnings": true,
        "edges": [
            [
                5,
                2,
                "This path leads to a blocking node from a non-blocking context",
                true,
                "stop-execution",
                2
            ]
        ]
    }
    ```

        Attributes:
            has_path_warnings (bool):
            edges (list['PathWarningsInfo']):
    """

    has_path_warnings: bool
    edges: list["PathWarningsInfo"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_path_warnings = self.has_path_warnings

        edges = []
        for edges_item_data in self.edges:
            edges_item = edges_item_data.to_dict()
            edges.append(edges_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_path_warnings": has_path_warnings,
                "edges": edges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.path_warnings_info import PathWarningsInfo

        d = dict(src_dict)
        has_path_warnings = d.pop("has_path_warnings")

        edges = []
        _edges = d.pop("edges")
        for edges_item_data in _edges:
            edges_item = PathWarningsInfo.from_dict(edges_item_data)

            edges.append(edges_item)

        path_warnings = cls(
            has_path_warnings=has_path_warnings,
            edges=edges,
        )

        path_warnings.additional_properties = d
        return path_warnings

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
