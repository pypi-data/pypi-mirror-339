from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_get_users_element_usersetting import PartialGetUsersElementUsersetting
    from ..models.partial_get_users_user import PartialGetUsersUser
    from ..models.partial_organisation_users_response import PartialOrganisationUsersResponse
    from ..models.partial_role_users_response import PartialRoleUsersResponse


T = TypeVar("T", bound="PartialGetUsersElement")


@_attrs_define
class PartialGetUsersElement:
    """
    Attributes:
        user (Union[Unset, PartialGetUsersUser]):
        role (Union[Unset, PartialRoleUsersResponse]):
        organisation (Union[Unset, PartialOrganisationUsersResponse]):
        user_setting (Union[Unset, PartialGetUsersElementUsersetting]):
    """

    user: Union[Unset, "PartialGetUsersUser"] = UNSET
    role: Union[Unset, "PartialRoleUsersResponse"] = UNSET
    organisation: Union[Unset, "PartialOrganisationUsersResponse"] = UNSET
    user_setting: Union[Unset, "PartialGetUsersElementUsersetting"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        role: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.to_dict()

        organisation: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.organisation, Unset):
            organisation = self.organisation.to_dict()

        user_setting: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_setting, Unset):
            user_setting = self.user_setting.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["User"] = user
        if role is not UNSET:
            field_dict["Role"] = role
        if organisation is not UNSET:
            field_dict["Organisation"] = organisation
        if user_setting is not UNSET:
            field_dict["UserSetting"] = user_setting

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partial_get_users_element_usersetting import PartialGetUsersElementUsersetting
        from ..models.partial_get_users_user import PartialGetUsersUser
        from ..models.partial_organisation_users_response import PartialOrganisationUsersResponse
        from ..models.partial_role_users_response import PartialRoleUsersResponse

        d = dict(src_dict)
        _user = d.pop("User", UNSET)
        user: Union[Unset, PartialGetUsersUser]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = PartialGetUsersUser.from_dict(_user)

        _role = d.pop("Role", UNSET)
        role: Union[Unset, PartialRoleUsersResponse]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = PartialRoleUsersResponse.from_dict(_role)

        _organisation = d.pop("Organisation", UNSET)
        organisation: Union[Unset, PartialOrganisationUsersResponse]
        if isinstance(_organisation, Unset):
            organisation = UNSET
        else:
            organisation = PartialOrganisationUsersResponse.from_dict(_organisation)

        _user_setting = d.pop("UserSetting", UNSET)
        user_setting: Union[Unset, PartialGetUsersElementUsersetting]
        if isinstance(_user_setting, Unset):
            user_setting = UNSET
        else:
            user_setting = PartialGetUsersElementUsersetting.from_dict(_user_setting)

        partial_get_users_element = cls(
            user=user,
            role=role,
            organisation=organisation,
            user_setting=user_setting,
        )

        partial_get_users_element.additional_properties = d
        return partial_get_users_element

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
