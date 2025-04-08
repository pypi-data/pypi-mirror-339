from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialTaxonomyView")


@_attrs_define
class PartialTaxonomyView:
    """
    Attributes:
        id (Union[Unset, int]):
        namespace (Union[Unset, str]):
        description (Union[Unset, str]):
        version (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        exclusive (Union[Unset, bool]):
        required (Union[Unset, bool]):
        highlighted (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    namespace: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    exclusive: Union[Unset, bool] = UNSET
    required: Union[Unset, bool] = UNSET
    highlighted: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        namespace = self.namespace

        description = self.description

        version = self.version

        enabled = self.enabled

        exclusive = self.exclusive

        required = self.required

        highlighted = self.highlighted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if description is not UNSET:
            field_dict["description"] = description
        if version is not UNSET:
            field_dict["version"] = version
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if exclusive is not UNSET:
            field_dict["exclusive"] = exclusive
        if required is not UNSET:
            field_dict["required"] = required
        if highlighted is not UNSET:
            field_dict["highlighted"] = highlighted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        namespace = d.pop("namespace", UNSET)

        description = d.pop("description", UNSET)

        version = d.pop("version", UNSET)

        enabled = d.pop("enabled", UNSET)

        exclusive = d.pop("exclusive", UNSET)

        required = d.pop("required", UNSET)

        highlighted = d.pop("highlighted", UNSET)

        partial_taxonomy_view = cls(
            id=id,
            namespace=namespace,
            description=description,
            version=version,
            enabled=enabled,
            exclusive=exclusive,
            required=required,
            highlighted=highlighted,
        )

        partial_taxonomy_view.additional_properties = d
        return partial_taxonomy_view

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
