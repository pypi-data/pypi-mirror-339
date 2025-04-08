from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.is_acyclic import IsAcyclic
    from ..models.miscellaneous_graph_validation_error import MiscellaneousGraphValidationError
    from ..models.multiple_output_connection import MultipleOutputConnection
    from ..models.path_warnings import PathWarnings


T = TypeVar("T", bound="CheckGraphResponse")


@_attrs_define
class CheckGraphResponse:
    """Response schema from the API for checking a graph.

    - **is_acyclic**: Indicates whether the graph is acyclic and provides information
      about the first detected cycle, if any.
    - **multiple_output_connection**: Indicates whether the graph has illegal multiple output connections,
    detailing the nodes involved.
    - **path_warnings**: Records warnings if a path leads to a blocking node from a
      'Concurrent Task' node, providing relevant details. Not used in Modern MISP, and will be returned empty.
    - **unsupported_modules"" List of the modules (identified with their graph_id) that are currently unsupported in
      Modern MISP (not yet implemented) causing the workflow to be invalid.
    - **misc_errors** Other miscellaneous errors indicating that the workflow graph is broken or etc. (edges registered
    at ports outside the valid range, inconsistencies between the incoming and outgoing adjacency lists etc.)

    Example JSON structure:
    ```json
    {
        "is_acyclic": {
            "is_acyclic": false,
            "cycles": [
                [4, 3, "Cycle"],
                [3, 4, "Cycle"]
            ]
        },
        "multiple_output_connection": {
            "has_multiple_output_connection": true,
            "edges": {
                "1": [5, 3]
            }
        },
        "path_warnings": {
            "has_path_warnings": true,
            "edges": [
                [5, 2, "This path leads to a blocking node from a non-blocking context", true, "stop-execution", 2]
            ]
        }
    }
    ```

        Attributes:
            is_acyclic (IsAcyclic): Represents the whether graph is acyclic and details of the first detected cycle.

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
            multiple_output_connection (MultipleOutputConnection): Represents the status and details of nodes with illegal
                multiple output connections in a graph.

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
            path_warnings (PathWarnings): Represents warnings for paths in a graph.

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
            unsupported_modules (list[int]):
            misc_errors (list['MiscellaneousGraphValidationError']):
    """

    is_acyclic: "IsAcyclic"
    multiple_output_connection: "MultipleOutputConnection"
    path_warnings: "PathWarnings"
    unsupported_modules: list[int]
    misc_errors: list["MiscellaneousGraphValidationError"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_acyclic = self.is_acyclic.to_dict()

        multiple_output_connection = self.multiple_output_connection.to_dict()

        path_warnings = self.path_warnings.to_dict()

        unsupported_modules = self.unsupported_modules

        misc_errors = []
        for misc_errors_item_data in self.misc_errors:
            misc_errors_item = misc_errors_item_data.to_dict()
            misc_errors.append(misc_errors_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_acyclic": is_acyclic,
                "multiple_output_connection": multiple_output_connection,
                "path_warnings": path_warnings,
                "unsupported_modules": unsupported_modules,
                "misc_errors": misc_errors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.is_acyclic import IsAcyclic
        from ..models.miscellaneous_graph_validation_error import MiscellaneousGraphValidationError
        from ..models.multiple_output_connection import MultipleOutputConnection
        from ..models.path_warnings import PathWarnings

        d = dict(src_dict)
        is_acyclic = IsAcyclic.from_dict(d.pop("is_acyclic"))

        multiple_output_connection = MultipleOutputConnection.from_dict(d.pop("multiple_output_connection"))

        path_warnings = PathWarnings.from_dict(d.pop("path_warnings"))

        unsupported_modules = cast(list[int], d.pop("unsupported_modules"))

        misc_errors = []
        _misc_errors = d.pop("misc_errors")
        for misc_errors_item_data in _misc_errors:
            misc_errors_item = MiscellaneousGraphValidationError.from_dict(misc_errors_item_data)

            misc_errors.append(misc_errors_item)

        check_graph_response = cls(
            is_acyclic=is_acyclic,
            multiple_output_connection=multiple_output_connection,
            path_warnings=path_warnings,
            unsupported_modules=unsupported_modules,
            misc_errors=misc_errors,
        )

        check_graph_response.additional_properties = d
        return check_graph_response

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
