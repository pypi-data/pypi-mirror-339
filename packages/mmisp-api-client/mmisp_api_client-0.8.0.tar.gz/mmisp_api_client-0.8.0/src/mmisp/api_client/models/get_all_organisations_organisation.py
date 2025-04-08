import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAllOrganisationsOrganisation")


@_attrs_define
class GetAllOrganisationsOrganisation:
    """
    Attributes:
        id (int):
        name (str):
        created_by (str):
        local (bool):
        user_count (int):
        created_by_email (str):
        nationality (Union[Unset, str]):
        sector (Union[Unset, str]):
        type_ (Union[Unset, str]):
        uuid (Union[Unset, str]):
        date_created (Union[Unset, datetime.datetime, str]):
        date_modified (Union[Unset, datetime.datetime, str]):
        description (Union[Unset, str]):
        contacts (Union[Unset, str]):
        restricted_to_domain (Union[Unset, list[Any], str]):
        landingpage (Union[Unset, str]):
    """

    id: int
    name: str
    created_by: str
    local: bool
    user_count: int
    created_by_email: str
    nationality: Union[Unset, str] = UNSET
    sector: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    uuid: Union[Unset, str] = UNSET
    date_created: Union[Unset, datetime.datetime, str] = UNSET
    date_modified: Union[Unset, datetime.datetime, str] = UNSET
    description: Union[Unset, str] = UNSET
    contacts: Union[Unset, str] = UNSET
    restricted_to_domain: Union[Unset, list[Any], str] = UNSET
    landingpage: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        created_by = self.created_by

        local = self.local

        user_count = self.user_count

        created_by_email = self.created_by_email

        nationality = self.nationality

        sector = self.sector

        type_ = self.type_

        uuid = self.uuid

        date_created: Union[Unset, str]
        if isinstance(self.date_created, Unset):
            date_created = UNSET
        elif isinstance(self.date_created, datetime.datetime):
            date_created = self.date_created.isoformat()
        else:
            date_created = self.date_created

        date_modified: Union[Unset, str]
        if isinstance(self.date_modified, Unset):
            date_modified = UNSET
        elif isinstance(self.date_modified, datetime.datetime):
            date_modified = self.date_modified.isoformat()
        else:
            date_modified = self.date_modified

        description = self.description

        contacts = self.contacts

        restricted_to_domain: Union[Unset, list[Any], str]
        if isinstance(self.restricted_to_domain, Unset):
            restricted_to_domain = UNSET
        elif isinstance(self.restricted_to_domain, list):
            restricted_to_domain = self.restricted_to_domain

        else:
            restricted_to_domain = self.restricted_to_domain

        landingpage = self.landingpage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "created_by": created_by,
                "local": local,
                "user_count": user_count,
                "created_by_email": created_by_email,
            }
        )
        if nationality is not UNSET:
            field_dict["nationality"] = nationality
        if sector is not UNSET:
            field_dict["sector"] = sector
        if type_ is not UNSET:
            field_dict["type"] = type_
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if date_created is not UNSET:
            field_dict["date_created"] = date_created
        if date_modified is not UNSET:
            field_dict["date_modified"] = date_modified
        if description is not UNSET:
            field_dict["description"] = description
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

        created_by = d.pop("created_by")

        local = d.pop("local")

        user_count = d.pop("user_count")

        created_by_email = d.pop("created_by_email")

        nationality = d.pop("nationality", UNSET)

        sector = d.pop("sector", UNSET)

        type_ = d.pop("type", UNSET)

        uuid = d.pop("uuid", UNSET)

        def _parse_date_created(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_created_type_0 = isoparse(data)

                return date_created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        date_created = _parse_date_created(d.pop("date_created", UNSET))

        def _parse_date_modified(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_modified_type_0 = isoparse(data)

                return date_modified_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        date_modified = _parse_date_modified(d.pop("date_modified", UNSET))

        description = d.pop("description", UNSET)

        contacts = d.pop("contacts", UNSET)

        def _parse_restricted_to_domain(data: object) -> Union[Unset, list[Any], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                restricted_to_domain_type_0 = cast(list[Any], data)

                return restricted_to_domain_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[Any], str], data)

        restricted_to_domain = _parse_restricted_to_domain(d.pop("restricted_to_domain", UNSET))

        landingpage = d.pop("landingpage", UNSET)

        get_all_organisations_organisation = cls(
            id=id,
            name=name,
            created_by=created_by,
            local=local,
            user_count=user_count,
            created_by_email=created_by_email,
            nationality=nationality,
            sector=sector,
            type_=type_,
            uuid=uuid,
            date_created=date_created,
            date_modified=date_modified,
            description=description,
            contacts=contacts,
            restricted_to_domain=restricted_to_domain,
            landingpage=landingpage,
        )

        get_all_organisations_organisation.additional_properties = d
        return get_all_organisations_organisation

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
