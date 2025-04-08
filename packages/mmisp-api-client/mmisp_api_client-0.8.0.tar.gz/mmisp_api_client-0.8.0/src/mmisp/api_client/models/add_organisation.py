from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddOrganisation")


@_attrs_define
class AddOrganisation:
    """
    Attributes:
        id (int):
        name (str):
        type_ (str):
        created_by (str):
        local (bool):
        description (Union[Unset, str]):
        nationality (Union[Unset, str]):
        sector (Union[Unset, str]):
        contacts (Union[Unset, str]):
        restricted_to_domain (Union[Unset, list[str]]):
        landingpage (Union[Unset, str]):
    """

    id: int
    name: str
    type_: str
    created_by: str
    local: bool
    description: Union[Unset, str] = UNSET
    nationality: Union[Unset, str] = UNSET
    sector: Union[Unset, str] = UNSET
    contacts: Union[Unset, str] = UNSET
    restricted_to_domain: Union[Unset, list[str]] = UNSET
    landingpage: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        type_ = self.type_

        created_by = self.created_by

        local = self.local

        description = self.description

        nationality = self.nationality

        sector = self.sector

        contacts = self.contacts

        restricted_to_domain: Union[Unset, list[str]] = UNSET
        if not isinstance(self.restricted_to_domain, Unset):
            restricted_to_domain = self.restricted_to_domain

        landingpage = self.landingpage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "type": type_,
                "created_by": created_by,
                "local": local,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if sector is not UNSET:
            field_dict["sector"] = sector
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if restricted_to_domain is not UNSET:
            field_dict["restricted_to_domain"] = restricted_to_domain
        if landingpage is not UNSET:
            field_dict["landingpage"] = landingpage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        type_ = d.pop("type")

        created_by = d.pop("created_by")

        local = d.pop("local")

        description = d.pop("description", UNSET)

        nationality = d.pop("nationality", UNSET)

        sector = d.pop("sector", UNSET)

        contacts = d.pop("contacts", UNSET)

        restricted_to_domain = cast(list[str], d.pop("restricted_to_domain", UNSET))

        landingpage = d.pop("landingpage", UNSET)

        add_organisation = cls(
            id=id,
            name=name,
            type_=type_,
            created_by=created_by,
            local=local,
            description=description,
            nationality=nationality,
            sector=sector,
            contacts=contacts,
            restricted_to_domain=restricted_to_domain,
            landingpage=landingpage,
        )

        add_organisation.additional_properties = d
        return add_organisation

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
