from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_galaxy_cluster_response import GetGalaxyClusterResponse
    from ..models.import_galaxy_galaxy import ImportGalaxyGalaxy


T = TypeVar("T", bound="ImportGalaxyBody")


@_attrs_define
class ImportGalaxyBody:
    """
    Attributes:
        galaxy_cluster (GetGalaxyClusterResponse):
        galaxy (ImportGalaxyGalaxy):
    """

    galaxy_cluster: "GetGalaxyClusterResponse"
    galaxy: "ImportGalaxyGalaxy"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        galaxy_cluster = self.galaxy_cluster.to_dict()

        galaxy = self.galaxy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "GalaxyCluster": galaxy_cluster,
                "Galaxy": galaxy,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_galaxy_cluster_response import GetGalaxyClusterResponse
        from ..models.import_galaxy_galaxy import ImportGalaxyGalaxy

        d = dict(src_dict)
        galaxy_cluster = GetGalaxyClusterResponse.from_dict(d.pop("GalaxyCluster"))

        galaxy = ImportGalaxyGalaxy.from_dict(d.pop("Galaxy"))

        import_galaxy_body = cls(
            galaxy_cluster=galaxy_cluster,
            galaxy=galaxy,
        )

        import_galaxy_body.additional_properties = d
        return import_galaxy_body

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
