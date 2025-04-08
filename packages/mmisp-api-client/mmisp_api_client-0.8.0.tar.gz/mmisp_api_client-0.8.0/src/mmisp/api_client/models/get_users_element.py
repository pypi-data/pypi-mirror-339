from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_users_element_usersetting import GetUsersElementUsersetting
    from ..models.get_users_user import GetUsersUser
    from ..models.organisation_users_response import OrganisationUsersResponse
    from ..models.role_users_response import RoleUsersResponse


T = TypeVar("T", bound="GetUsersElement")


@_attrs_define
class GetUsersElement:
    """
    Attributes:
        user (GetUsersUser):
        role (RoleUsersResponse):
        organisation (OrganisationUsersResponse):
        user_setting (Union[Unset, GetUsersElementUsersetting]):
    """

    user: "GetUsersUser"
    role: "RoleUsersResponse"
    organisation: "OrganisationUsersResponse"
    user_setting: Union[Unset, "GetUsersElementUsersetting"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user.to_dict()

        role = self.role.to_dict()

        organisation = self.organisation.to_dict()

        user_setting: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_setting, Unset):
            user_setting = self.user_setting.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "User": user,
                "Role": role,
                "Organisation": organisation,
            }
        )
        if user_setting is not UNSET:
            field_dict["UserSetting"] = user_setting

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_users_element_usersetting import GetUsersElementUsersetting
        from ..models.get_users_user import GetUsersUser
        from ..models.organisation_users_response import OrganisationUsersResponse
        from ..models.role_users_response import RoleUsersResponse

        d = dict(src_dict)
        user = GetUsersUser.from_dict(d.pop("User"))

        role = RoleUsersResponse.from_dict(d.pop("Role"))

        organisation = OrganisationUsersResponse.from_dict(d.pop("Organisation"))

        _user_setting = d.pop("UserSetting", UNSET)
        user_setting: Union[Unset, GetUsersElementUsersetting]
        if isinstance(_user_setting, Unset):
            user_setting = UNSET
        else:
            user_setting = GetUsersElementUsersetting.from_dict(_user_setting)

        get_users_element = cls(
            user=user,
            role=role,
            organisation=organisation,
            user_setting=user_setting,
        )

        get_users_element.additional_properties = d
        return get_users_element

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
