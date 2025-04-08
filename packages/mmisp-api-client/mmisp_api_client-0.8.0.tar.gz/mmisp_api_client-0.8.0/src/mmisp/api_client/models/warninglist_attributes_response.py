from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.warninglist_entry_response import WarninglistEntryResponse
    from ..models.warninglist_type_response import WarninglistTypeResponse


T = TypeVar("T", bound="WarninglistAttributesResponse")


@_attrs_define
class WarninglistAttributesResponse:
    """
    Attributes:
        id (int):
        name (str):
        type_ (str):
        description (str):
        version (str):
        enabled (bool):
        default (bool):
        category (str):
        warninglist_entry (Union[Unset, list['WarninglistEntryResponse']]):
        warninglist_type (Union[Unset, list['WarninglistTypeResponse']]):
    """

    id: int
    name: str
    type_: str
    description: str
    version: str
    enabled: bool
    default: bool
    category: str
    warninglist_entry: Union[Unset, list["WarninglistEntryResponse"]] = UNSET
    warninglist_type: Union[Unset, list["WarninglistTypeResponse"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        type_ = self.type_

        description = self.description

        version = self.version

        enabled = self.enabled

        default = self.default

        category = self.category

        warninglist_entry: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.warninglist_entry, Unset):
            warninglist_entry = []
            for warninglist_entry_item_data in self.warninglist_entry:
                warninglist_entry_item = warninglist_entry_item_data.to_dict()
                warninglist_entry.append(warninglist_entry_item)

        warninglist_type: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.warninglist_type, Unset):
            warninglist_type = []
            for warninglist_type_item_data in self.warninglist_type:
                warninglist_type_item = warninglist_type_item_data.to_dict()
                warninglist_type.append(warninglist_type_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "description": description,
                "version": version,
                "enabled": enabled,
                "default": default,
                "category": category,
            }
        )
        if warninglist_entry is not UNSET:
            field_dict["WarninglistEntry"] = warninglist_entry
        if warninglist_type is not UNSET:
            field_dict["WarninglistType"] = warninglist_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.warninglist_entry_response import WarninglistEntryResponse
        from ..models.warninglist_type_response import WarninglistTypeResponse

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        type_ = d.pop("type")

        description = d.pop("description")

        version = d.pop("version")

        enabled = d.pop("enabled")

        default = d.pop("default")

        category = d.pop("category")

        warninglist_entry = []
        _warninglist_entry = d.pop("WarninglistEntry", UNSET)
        for warninglist_entry_item_data in _warninglist_entry or []:
            warninglist_entry_item = WarninglistEntryResponse.from_dict(warninglist_entry_item_data)

            warninglist_entry.append(warninglist_entry_item)

        warninglist_type = []
        _warninglist_type = d.pop("WarninglistType", UNSET)
        for warninglist_type_item_data in _warninglist_type or []:
            warninglist_type_item = WarninglistTypeResponse.from_dict(warninglist_type_item_data)

            warninglist_type.append(warninglist_type_item)

        warninglist_attributes_response = cls(
            id=id,
            name=name,
            type_=type_,
            description=description,
            version=version,
            enabled=enabled,
            default=default,
            category=category,
            warninglist_entry=warninglist_entry,
            warninglist_type=warninglist_type,
        )

        warninglist_attributes_response.additional_properties = d
        return warninglist_attributes_response

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
