from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_describe_types_attributes import GetDescribeTypesAttributes


T = TypeVar("T", bound="GetDescribeTypesResponse")


@_attrs_define
class GetDescribeTypesResponse:
    """
    Attributes:
        result (GetDescribeTypesAttributes):
    """

    result: "GetDescribeTypesAttributes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = self.result.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "result": result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_describe_types_attributes import GetDescribeTypesAttributes

        d = dict(src_dict)
        result = GetDescribeTypesAttributes.from_dict(d.pop("result"))

        get_describe_types_response = cls(
            result=result,
        )

        get_describe_types_response.additional_properties = d
        return get_describe_types_response

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
