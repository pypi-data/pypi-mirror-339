from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.object_with_attributes_response import ObjectWithAttributesResponse


T = TypeVar("T", bound="ObjectResponse")


@_attrs_define
class ObjectResponse:
    """
    Attributes:
        object_ (ObjectWithAttributesResponse):
    """

    object_: "ObjectWithAttributesResponse"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        object_ = self.object_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.object_with_attributes_response import ObjectWithAttributesResponse

        d = dict(src_dict)
        object_ = ObjectWithAttributesResponse.from_dict(d.pop("Object"))

        object_response = cls(
            object_=object_,
        )

        object_response.additional_properties = d
        return object_response

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
