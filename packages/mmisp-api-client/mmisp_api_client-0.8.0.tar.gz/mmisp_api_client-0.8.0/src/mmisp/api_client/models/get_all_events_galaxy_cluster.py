from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_galaxy_cluster_meta import AddEditGetEventGalaxyClusterMeta
    from ..models.get_all_events_galaxy_cluster_galaxy import GetAllEventsGalaxyClusterGalaxy


T = TypeVar("T", bound="GetAllEventsGalaxyCluster")


@_attrs_define
class GetAllEventsGalaxyCluster:
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
        org_id (int):
        orgc_id (int):
        extends_uuid (str):
        extends_version (str):
        galaxy (GetAllEventsGalaxyClusterGalaxy):
        tag_id (int):
        distribution (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        default (Union[Unset, str]):
        locked (Union[Unset, bool]):
        published (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        meta (Union[Unset, AddEditGetEventGalaxyClusterMeta]):
        local (Union[Unset, bool]):
        relationship_type (Union[Unset, bool, str]):
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
    org_id: int
    orgc_id: int
    extends_uuid: str
    extends_version: str
    galaxy: "GetAllEventsGalaxyClusterGalaxy"
    tag_id: int
    distribution: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    default: Union[Unset, str] = UNSET
    locked: Union[Unset, bool] = UNSET
    published: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    meta: Union[Unset, "AddEditGetEventGalaxyClusterMeta"] = UNSET
    local: Union[Unset, bool] = UNSET
    relationship_type: Union[Unset, bool, str] = UNSET
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

        org_id = self.org_id

        orgc_id = self.orgc_id

        extends_uuid = self.extends_uuid

        extends_version = self.extends_version

        galaxy = self.galaxy.to_dict()

        tag_id = self.tag_id

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        default = self.default

        locked = self.locked

        published = self.published

        deleted = self.deleted

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        local = self.local

        relationship_type: Union[Unset, bool, str]
        if isinstance(self.relationship_type, Unset):
            relationship_type = UNSET
        else:
            relationship_type = self.relationship_type

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
                "org_id": org_id,
                "orgc_id": orgc_id,
                "extends_uuid": extends_uuid,
                "extends_version": extends_version,
                "Galaxy": galaxy,
                "tag_id": tag_id,
            }
        )
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if default is not UNSET:
            field_dict["default"] = default
        if locked is not UNSET:
            field_dict["locked"] = locked
        if published is not UNSET:
            field_dict["published"] = published
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if meta is not UNSET:
            field_dict["meta"] = meta
        if local is not UNSET:
            field_dict["local"] = local
        if relationship_type is not UNSET:
            field_dict["relationship_type"] = relationship_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_galaxy_cluster_meta import AddEditGetEventGalaxyClusterMeta
        from ..models.get_all_events_galaxy_cluster_galaxy import GetAllEventsGalaxyClusterGalaxy

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

        org_id = d.pop("org_id")

        orgc_id = d.pop("orgc_id")

        extends_uuid = d.pop("extends_uuid")

        extends_version = d.pop("extends_version")

        galaxy = GetAllEventsGalaxyClusterGalaxy.from_dict(d.pop("Galaxy"))

        tag_id = d.pop("tag_id")

        distribution = d.pop("distribution", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        default = d.pop("default", UNSET)

        locked = d.pop("locked", UNSET)

        published = d.pop("published", UNSET)

        deleted = d.pop("deleted", UNSET)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, AddEditGetEventGalaxyClusterMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = AddEditGetEventGalaxyClusterMeta.from_dict(_meta)

        local = d.pop("local", UNSET)

        def _parse_relationship_type(data: object) -> Union[Unset, bool, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, bool, str], data)

        relationship_type = _parse_relationship_type(d.pop("relationship_type", UNSET))

        get_all_events_galaxy_cluster = cls(
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
            org_id=org_id,
            orgc_id=orgc_id,
            extends_uuid=extends_uuid,
            extends_version=extends_version,
            galaxy=galaxy,
            tag_id=tag_id,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            default=default,
            locked=locked,
            published=published,
            deleted=deleted,
            meta=meta,
            local=local,
            relationship_type=relationship_type,
        )

        get_all_events_galaxy_cluster.additional_properties = d
        return get_all_events_galaxy_cluster

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
