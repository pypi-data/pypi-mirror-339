from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ObjectTemplatesRequirements")


@_attrs_define
class ObjectTemplatesRequirements:
    """
    Attributes:
        required_one_of (Union[Unset, list[str]]):
        required (Union[Unset, list[str]]):
    """

    required_one_of: Union[Unset, list[str]] = UNSET
    required: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        required_one_of: Union[Unset, list[str]] = UNSET
        if not isinstance(self.required_one_of, Unset):
            required_one_of = self.required_one_of

        required: Union[Unset, list[str]] = UNSET
        if not isinstance(self.required, Unset):
            required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_one_of is not UNSET:
            field_dict["requiredOneOf"] = required_one_of
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        required_one_of = cast(list[str], d.pop("requiredOneOf", UNSET))

        required = cast(list[str], d.pop("required", UNSET))

        object_templates_requirements = cls(
            required_one_of=required_one_of,
            required=required,
        )

        object_templates_requirements.additional_properties = d
        return object_templates_requirements

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
