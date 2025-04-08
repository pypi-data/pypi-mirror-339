from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.base_organisation import BaseOrganisation
    from ..models.server_response import ServerResponse


T = TypeVar("T", bound="GetRemoteServer")


@_attrs_define
class GetRemoteServer:
    """
    Attributes:
        server (ServerResponse):
        organisation (BaseOrganisation):
        remote_org (BaseOrganisation):
        user (list[Any]):
    """

    server: "ServerResponse"
    organisation: "BaseOrganisation"
    remote_org: "BaseOrganisation"
    user: list[Any]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        server = self.server.to_dict()

        organisation = self.organisation.to_dict()

        remote_org = self.remote_org.to_dict()

        user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Server": server,
                "Organisation": organisation,
                "RemoteOrg": remote_org,
                "User": user,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_organisation import BaseOrganisation
        from ..models.server_response import ServerResponse

        d = dict(src_dict)
        server = ServerResponse.from_dict(d.pop("Server"))

        organisation = BaseOrganisation.from_dict(d.pop("Organisation"))

        remote_org = BaseOrganisation.from_dict(d.pop("RemoteOrg"))

        user = cast(list[Any], d.pop("User"))

        get_remote_server = cls(
            server=server,
            organisation=organisation,
            remote_org=remote_org,
            user=user,
        )

        get_remote_server.additional_properties = d
        return get_remote_server

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
