from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sighting_organisation_response import SightingOrganisationResponse


T = TypeVar("T", bound="SightingAttributesResponse")


@_attrs_define
class SightingAttributesResponse:
    """
    Attributes:
        id (int):
        uuid (str):
        attribute_id (int):
        attribute_uuid (str):
        event_id (Union[Unset, int]):
        org_id (Union[Unset, int]):
        date_sighting (Union[Unset, str]):
        source (Union[Unset, str]):
        type_ (Union[Unset, str]):
        organisation (Union[Unset, SightingOrganisationResponse]):
    """

    id: int
    uuid: str
    attribute_id: int
    attribute_uuid: str
    event_id: Union[Unset, int] = UNSET
    org_id: Union[Unset, int] = UNSET
    date_sighting: Union[Unset, str] = UNSET
    source: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    organisation: Union[Unset, "SightingOrganisationResponse"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        attribute_id = self.attribute_id

        attribute_uuid = self.attribute_uuid

        event_id = self.event_id

        org_id = self.org_id

        date_sighting = self.date_sighting

        source = self.source

        type_ = self.type_

        organisation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.organisation, Unset):
            organisation = self.organisation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "attribute_id": attribute_id,
                "attribute_uuid": attribute_uuid,
            }
        )
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if date_sighting is not UNSET:
            field_dict["date_sighting"] = date_sighting
        if source is not UNSET:
            field_dict["source"] = source
        if type_ is not UNSET:
            field_dict["type"] = type_
        if organisation is not UNSET:
            field_dict["Organisation"] = organisation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sighting_organisation_response import SightingOrganisationResponse

        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        attribute_id = d.pop("attribute_id")

        attribute_uuid = d.pop("attribute_uuid")

        event_id = d.pop("event_id", UNSET)

        org_id = d.pop("org_id", UNSET)

        date_sighting = d.pop("date_sighting", UNSET)

        source = d.pop("source", UNSET)

        type_ = d.pop("type", UNSET)

        _organisation = d.pop("Organisation", UNSET)
        organisation: Union[Unset, SightingOrganisationResponse]
        if isinstance(_organisation, Unset):
            organisation = UNSET
        else:
            organisation = SightingOrganisationResponse.from_dict(_organisation)

        sighting_attributes_response = cls(
            id=id,
            uuid=uuid,
            attribute_id=attribute_id,
            attribute_uuid=attribute_uuid,
            event_id=event_id,
            org_id=org_id,
            date_sighting=date_sighting,
            source=source,
            type_=type_,
            organisation=organisation,
        )

        sighting_attributes_response.additional_properties = d
        return sighting_attributes_response

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
