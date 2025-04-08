from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.export_galaxy_galaxy_element import ExportGalaxyGalaxyElement


T = TypeVar("T", bound="GetGalaxyClusterResponse")


@_attrs_define
class GetGalaxyClusterResponse:
    """
    Attributes:
        id (int):
        uuid (str):
        collection_uuid (str):
        type_ (str):
        value (str):
        tag_name (str):
        description (str):
        galaxy_id (int):
        source (str):
        authors (list[str]):
        version (str):
        distribution (str):
        sharing_group_id (int):
        org_id (int):
        orgc_id (int):
        default (bool):
        locked (bool):
        extends_uuid (str):
        extends_version (str):
        published (bool):
        deleted (bool):
        galaxy_element (list['ExportGalaxyGalaxyElement']):
    """

    id: int
    uuid: str
    collection_uuid: str
    type_: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: str
    distribution: str
    sharing_group_id: int
    org_id: int
    orgc_id: int
    default: bool
    locked: bool
    extends_uuid: str
    extends_version: str
    published: bool
    deleted: bool
    galaxy_element: list["ExportGalaxyGalaxyElement"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        uuid = self.uuid

        collection_uuid = self.collection_uuid

        type_ = self.type_

        value = self.value

        tag_name = self.tag_name

        description = self.description

        galaxy_id = self.galaxy_id

        source = self.source

        authors = self.authors

        version = self.version

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        org_id = self.org_id

        orgc_id = self.orgc_id

        default = self.default

        locked = self.locked

        extends_uuid = self.extends_uuid

        extends_version = self.extends_version

        published = self.published

        deleted = self.deleted

        galaxy_element = []
        for galaxy_element_item_data in self.galaxy_element:
            galaxy_element_item = galaxy_element_item_data.to_dict()
            galaxy_element.append(galaxy_element_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "collection_uuid": collection_uuid,
                "type": type_,
                "value": value,
                "tag_name": tag_name,
                "description": description,
                "galaxy_id": galaxy_id,
                "source": source,
                "authors": authors,
                "version": version,
                "distribution": distribution,
                "sharing_group_id": sharing_group_id,
                "org_id": org_id,
                "orgc_id": orgc_id,
                "default": default,
                "locked": locked,
                "extends_uuid": extends_uuid,
                "extends_version": extends_version,
                "published": published,
                "deleted": deleted,
                "GalaxyElement": galaxy_element,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_galaxy_galaxy_element import ExportGalaxyGalaxyElement

        d = dict(src_dict)
        id = d.pop("id")

        uuid = d.pop("uuid")

        collection_uuid = d.pop("collection_uuid")

        type_ = d.pop("type")

        value = d.pop("value")

        tag_name = d.pop("tag_name")

        description = d.pop("description")

        galaxy_id = d.pop("galaxy_id")

        source = d.pop("source")

        authors = cast(list[str], d.pop("authors"))

        version = d.pop("version")

        distribution = d.pop("distribution")

        sharing_group_id = d.pop("sharing_group_id")

        org_id = d.pop("org_id")

        orgc_id = d.pop("orgc_id")

        default = d.pop("default")

        locked = d.pop("locked")

        extends_uuid = d.pop("extends_uuid")

        extends_version = d.pop("extends_version")

        published = d.pop("published")

        deleted = d.pop("deleted")

        galaxy_element = []
        _galaxy_element = d.pop("GalaxyElement")
        for galaxy_element_item_data in _galaxy_element:
            galaxy_element_item = ExportGalaxyGalaxyElement.from_dict(galaxy_element_item_data)

            galaxy_element.append(galaxy_element_item)

        get_galaxy_cluster_response = cls(
            id=id,
            uuid=uuid,
            collection_uuid=collection_uuid,
            type_=type_,
            value=value,
            tag_name=tag_name,
            description=description,
            galaxy_id=galaxy_id,
            source=source,
            authors=authors,
            version=version,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            org_id=org_id,
            orgc_id=orgc_id,
            default=default,
            locked=locked,
            extends_uuid=extends_uuid,
            extends_version=extends_version,
            published=published,
            deleted=deleted,
            galaxy_element=galaxy_element,
        )

        get_galaxy_cluster_response.additional_properties = d
        return get_galaxy_cluster_response

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
