from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sharing_group_org_organisation_index_info import SharingGroupOrgOrganisationIndexInfo


T = TypeVar("T", bound="SharingGroupOrgIndexItem")


@_attrs_define
class SharingGroupOrgIndexItem:
    """
    Attributes:
        id (int):
        sharing_group_id (int):
        org_id (int):
        extend (bool):
        organisation (SharingGroupOrgOrganisationIndexInfo):
    """

    id: int
    sharing_group_id: int
    org_id: int
    extend: bool
    organisation: "SharingGroupOrgOrganisationIndexInfo"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        sharing_group_id = self.sharing_group_id

        org_id = self.org_id

        extend = self.extend

        organisation = self.organisation.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "sharing_group_id": sharing_group_id,
                "org_id": org_id,
                "extend": extend,
                "Organisation": organisation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sharing_group_org_organisation_index_info import SharingGroupOrgOrganisationIndexInfo

        d = dict(src_dict)
        id = d.pop("id")

        sharing_group_id = d.pop("sharing_group_id")

        org_id = d.pop("org_id")

        extend = d.pop("extend")

        organisation = SharingGroupOrgOrganisationIndexInfo.from_dict(d.pop("Organisation"))

        sharing_group_org_index_item = cls(
            id=id,
            sharing_group_id=sharing_group_id,
            org_id=org_id,
            extend=extend,
            organisation=organisation,
        )

        sharing_group_org_index_item.additional_properties = d
        return sharing_group_org_index_item

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
