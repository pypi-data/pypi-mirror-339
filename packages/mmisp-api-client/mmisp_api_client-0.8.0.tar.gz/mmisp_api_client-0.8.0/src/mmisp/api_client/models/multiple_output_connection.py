from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.multiple_output_connection_edges import MultipleOutputConnectionEdges


T = TypeVar("T", bound="MultipleOutputConnection")


@_attrs_define
class MultipleOutputConnection:
    """Represents the status and details of nodes with illegal multiple output connections in a graph.

    - **has_multiple_output_connection**: True if at least one node has multiple output
      connections that are not allowed.
      For example, the 'Concurrent Task' node can have multiple output connections while the value here is `False`.
    - **edges**: A dictionary where the key is the ID of a node with multiple illegal connections,
      and the value is a list of node IDs to which these illegal connections are made.

    Example:
    ```json
    "multiple_output_connection": {
        "has_multiple_output_connection": true,
        "edges": {
            "1": [
                5,
                3
            ]
        }
    }
    ```

        Attributes:
            has_multiple_output_connection (bool):
            edges (MultipleOutputConnectionEdges):
    """

    has_multiple_output_connection: bool
    edges: "MultipleOutputConnectionEdges"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_multiple_output_connection = self.has_multiple_output_connection

        edges = self.edges.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_multiple_output_connection": has_multiple_output_connection,
                "edges": edges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multiple_output_connection_edges import MultipleOutputConnectionEdges

        d = dict(src_dict)
        has_multiple_output_connection = d.pop("has_multiple_output_connection")

        edges = MultipleOutputConnectionEdges.from_dict(d.pop("edges"))

        multiple_output_connection = cls(
            has_multiple_output_connection=has_multiple_output_connection,
            edges=edges,
        )

        multiple_output_connection.additional_properties = d
        return multiple_output_connection

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
