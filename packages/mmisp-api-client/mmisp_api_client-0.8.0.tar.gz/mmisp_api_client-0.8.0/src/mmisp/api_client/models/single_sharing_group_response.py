from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.organisation import Organisation
    from ..models.sharing_group import SharingGroup
    from ..models.view_update_sharing_group_legacy_response_sharing_group_org_item import (
        ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem,
    )
    from ..models.view_update_sharing_group_legacy_response_sharing_group_server_item import (
        ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem,
    )


T = TypeVar("T", bound="SingleSharingGroupResponse")


@_attrs_define
class SingleSharingGroupResponse:
    """
    Attributes:
        sharing_group (SharingGroup):
        organisation (Organisation):
        sharing_group_org (list['ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem']):
        sharing_group_server (list['ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem']):
    """

    sharing_group: "SharingGroup"
    organisation: "Organisation"
    sharing_group_org: list["ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem"]
    sharing_group_server: list["ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sharing_group = self.sharing_group.to_dict()

        organisation = self.organisation.to_dict()

        sharing_group_org = []
        for sharing_group_org_item_data in self.sharing_group_org:
            sharing_group_org_item = sharing_group_org_item_data.to_dict()
            sharing_group_org.append(sharing_group_org_item)

        sharing_group_server = []
        for sharing_group_server_item_data in self.sharing_group_server:
            sharing_group_server_item = sharing_group_server_item_data.to_dict()
            sharing_group_server.append(sharing_group_server_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "SharingGroup": sharing_group,
                "Organisation": organisation,
                "SharingGroupOrg": sharing_group_org,
                "SharingGroupServer": sharing_group_server,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organisation import Organisation
        from ..models.sharing_group import SharingGroup
        from ..models.view_update_sharing_group_legacy_response_sharing_group_org_item import (
            ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem,
        )
        from ..models.view_update_sharing_group_legacy_response_sharing_group_server_item import (
            ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem,
        )

        d = dict(src_dict)
        sharing_group = SharingGroup.from_dict(d.pop("SharingGroup"))

        organisation = Organisation.from_dict(d.pop("Organisation"))

        sharing_group_org = []
        _sharing_group_org = d.pop("SharingGroupOrg")
        for sharing_group_org_item_data in _sharing_group_org:
            sharing_group_org_item = ViewUpdateSharingGroupLegacyResponseSharingGroupOrgItem.from_dict(
                sharing_group_org_item_data
            )

            sharing_group_org.append(sharing_group_org_item)

        sharing_group_server = []
        _sharing_group_server = d.pop("SharingGroupServer")
        for sharing_group_server_item_data in _sharing_group_server:
            sharing_group_server_item = ViewUpdateSharingGroupLegacyResponseSharingGroupServerItem.from_dict(
                sharing_group_server_item_data
            )

            sharing_group_server.append(sharing_group_server_item)

        single_sharing_group_response = cls(
            sharing_group=sharing_group,
            organisation=organisation,
            sharing_group_org=sharing_group_org,
            sharing_group_server=sharing_group_server,
        )

        single_sharing_group_response.additional_properties = d
        return single_sharing_group_response

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
