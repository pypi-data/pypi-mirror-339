from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseOrganisation")


@_attrs_define
class BaseOrganisation:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        nationality (Union[Unset, str]):
        sector (Union[Unset, str]):
        type_ (Union[Unset, str]):
        uuid (Union[Unset, str]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    nationality: Union[Unset, str] = UNSET
    sector: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        nationality = self.nationality

        sector = self.sector

        type_ = self.type_

        uuid = self.uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if sector is not UNSET:
            field_dict["sector"] = sector
        if type_ is not UNSET:
            field_dict["type"] = type_
        if uuid is not UNSET:
            field_dict["uuid"] = uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        nationality = d.pop("nationality", UNSET)

        sector = d.pop("sector", UNSET)

        type_ = d.pop("type", UNSET)

        uuid = d.pop("uuid", UNSET)

        base_organisation = cls(
            id=id,
            name=name,
            nationality=nationality,
            sector=sector,
            type_=type_,
            uuid=uuid,
        )

        base_organisation.additional_properties = d
        return base_organisation

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
