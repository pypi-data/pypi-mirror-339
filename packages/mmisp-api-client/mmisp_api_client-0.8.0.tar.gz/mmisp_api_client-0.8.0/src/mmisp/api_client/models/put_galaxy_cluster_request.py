from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.distribution_levels import DistributionLevels

if TYPE_CHECKING:
    from ..models.add_update_galaxy_element import AddUpdateGalaxyElement


T = TypeVar("T", bound="PutGalaxyClusterRequest")


@_attrs_define
class PutGalaxyClusterRequest:
    """
    Attributes:
        id (int):
        value (str):
        description (str):
        source (str):
        type_ (str):
        uuid (UUID):
        version (int):
        authors (list[str]):
        distribution (DistributionLevels): An enumeration.
        galaxy_element (list['AddUpdateGalaxyElement']):
    """

    id: int
    value: str
    description: str
    source: str
    type_: str
    uuid: UUID
    version: int
    authors: list[str]
    distribution: DistributionLevels
    galaxy_element: list["AddUpdateGalaxyElement"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        value = self.value

        description = self.description

        source = self.source

        type_ = self.type_

        uuid = str(self.uuid)

        version = self.version

        authors = self.authors

        distribution = self.distribution.value

        galaxy_element = []
        for galaxy_element_item_data in self.galaxy_element:
            galaxy_element_item = galaxy_element_item_data.to_dict()
            galaxy_element.append(galaxy_element_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
                "description": description,
                "source": source,
                "type": type_,
                "uuid": uuid,
                "version": version,
                "authors": authors,
                "distribution": distribution,
                "GalaxyElement": galaxy_element,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_update_galaxy_element import AddUpdateGalaxyElement

        d = dict(src_dict)
        id = d.pop("id")

        value = d.pop("value")

        description = d.pop("description")

        source = d.pop("source")

        type_ = d.pop("type")

        uuid = UUID(d.pop("uuid"))

        version = d.pop("version")

        authors = cast(list[str], d.pop("authors"))

        distribution = DistributionLevels(d.pop("distribution"))

        galaxy_element = []
        _galaxy_element = d.pop("GalaxyElement")
        for galaxy_element_item_data in _galaxy_element:
            galaxy_element_item = AddUpdateGalaxyElement.from_dict(galaxy_element_item_data)

            galaxy_element.append(galaxy_element_item)

        put_galaxy_cluster_request = cls(
            id=id,
            value=value,
            description=description,
            source=source,
            type_=type_,
            uuid=uuid,
            version=version,
            authors=authors,
            distribution=distribution,
            galaxy_element=galaxy_element,
        )

        put_galaxy_cluster_request.additional_properties = d
        return put_galaxy_cluster_request

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
