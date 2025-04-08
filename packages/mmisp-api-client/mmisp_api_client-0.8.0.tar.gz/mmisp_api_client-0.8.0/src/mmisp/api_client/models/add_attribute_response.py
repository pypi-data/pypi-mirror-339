from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.add_attribute_attributes import AddAttributeAttributes


T = TypeVar("T", bound="AddAttributeResponse")


@_attrs_define
class AddAttributeResponse:
    """
    Attributes:
        attribute (AddAttributeAttributes):
    """

    attribute: "AddAttributeAttributes"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attribute = self.attribute.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Attribute": attribute,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_attribute_attributes import AddAttributeAttributes

        d = dict(src_dict)
        attribute = AddAttributeAttributes.from_dict(d.pop("Attribute"))

        add_attribute_response = cls(
            attribute=attribute,
        )

        add_attribute_response.additional_properties = d
        return add_attribute_response

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
