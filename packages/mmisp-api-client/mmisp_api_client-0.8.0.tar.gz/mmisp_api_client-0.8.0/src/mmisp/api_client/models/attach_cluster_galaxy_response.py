from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AttachClusterGalaxyResponse")


@_attrs_define
class AttachClusterGalaxyResponse:
    """
    Attributes:
        saved (bool):
        success (str):
        check_publish (bool):
    """

    saved: bool
    success: str
    check_publish: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        saved = self.saved

        success = self.success

        check_publish = self.check_publish

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "saved": saved,
                "success": success,
                "check_publish": check_publish,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        saved = d.pop("saved")

        success = d.pop("success")

        check_publish = d.pop("check_publish")

        attach_cluster_galaxy_response = cls(
            saved=saved,
            success=success,
            check_publish=check_publish,
        )

        attach_cluster_galaxy_response.additional_properties = d
        return attach_cluster_galaxy_response

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
