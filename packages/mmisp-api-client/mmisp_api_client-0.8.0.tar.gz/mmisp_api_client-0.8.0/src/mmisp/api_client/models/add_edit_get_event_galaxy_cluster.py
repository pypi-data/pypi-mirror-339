from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_galaxy_cluster_meta import AddEditGetEventGalaxyClusterMeta
    from ..models.add_edit_get_event_galaxy_cluster_relation import AddEditGetEventGalaxyClusterRelation
    from ..models.organisation import Organisation


T = TypeVar("T", bound="AddEditGetEventGalaxyCluster")


@_attrs_define
class AddEditGetEventGalaxyCluster:
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
        tag_id (int):
        distribution (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        default (Union[Unset, bool]):
        locked (Union[Unset, bool]):
        extends_uuid (Union[Unset, str]):
        extends_version (Union[Unset, str]):
        published (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        galaxy_cluster_relation (Union[Unset, list['AddEditGetEventGalaxyClusterRelation']]):
        org (Union[Unset, Organisation]):
        orgc (Union[Unset, Organisation]):
        meta (Union[Unset, AddEditGetEventGalaxyClusterMeta]):
        attribute_tag_id (Union[Unset, int]):
        event_tag_id (Union[Unset, int]):
        local (Union[Unset, bool]):
        relationship_type (Union[Unset, bool, str]):  Default: ''.
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
    tag_id: int
    distribution: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    default: Union[Unset, bool] = UNSET
    locked: Union[Unset, bool] = UNSET
    extends_uuid: Union[Unset, str] = UNSET
    extends_version: Union[Unset, str] = UNSET
    published: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    galaxy_cluster_relation: Union[Unset, list["AddEditGetEventGalaxyClusterRelation"]] = UNSET
    org: Union[Unset, "Organisation"] = UNSET
    orgc: Union[Unset, "Organisation"] = UNSET
    meta: Union[Unset, "AddEditGetEventGalaxyClusterMeta"] = UNSET
    attribute_tag_id: Union[Unset, int] = UNSET
    event_tag_id: Union[Unset, int] = UNSET
    local: Union[Unset, bool] = UNSET
    relationship_type: Union[Unset, bool, str] = ""
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

        tag_id = self.tag_id

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        default = self.default

        locked = self.locked

        extends_uuid = self.extends_uuid

        extends_version = self.extends_version

        published = self.published

        deleted = self.deleted

        galaxy_cluster_relation: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.galaxy_cluster_relation, Unset):
            galaxy_cluster_relation = []
            for galaxy_cluster_relation_item_data in self.galaxy_cluster_relation:
                galaxy_cluster_relation_item = galaxy_cluster_relation_item_data.to_dict()
                galaxy_cluster_relation.append(galaxy_cluster_relation_item)

        org: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.org, Unset):
            org = self.org.to_dict()

        orgc: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.orgc, Unset):
            orgc = self.orgc.to_dict()

        meta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.meta, Unset):
            meta = self.meta.to_dict()

        attribute_tag_id = self.attribute_tag_id

        event_tag_id = self.event_tag_id

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
        if extends_uuid is not UNSET:
            field_dict["extends_uuid"] = extends_uuid
        if extends_version is not UNSET:
            field_dict["extends_version"] = extends_version
        if published is not UNSET:
            field_dict["published"] = published
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if galaxy_cluster_relation is not UNSET:
            field_dict["GalaxyClusterRelation"] = galaxy_cluster_relation
        if org is not UNSET:
            field_dict["Org"] = org
        if orgc is not UNSET:
            field_dict["Orgc"] = orgc
        if meta is not UNSET:
            field_dict["meta"] = meta
        if attribute_tag_id is not UNSET:
            field_dict["attribute_tag_id"] = attribute_tag_id
        if event_tag_id is not UNSET:
            field_dict["event_tag_id"] = event_tag_id
        if local is not UNSET:
            field_dict["local"] = local
        if relationship_type is not UNSET:
            field_dict["relationship_type"] = relationship_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_galaxy_cluster_meta import AddEditGetEventGalaxyClusterMeta
        from ..models.add_edit_get_event_galaxy_cluster_relation import AddEditGetEventGalaxyClusterRelation
        from ..models.organisation import Organisation

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

        tag_id = d.pop("tag_id")

        distribution = d.pop("distribution", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        default = d.pop("default", UNSET)

        locked = d.pop("locked", UNSET)

        extends_uuid = d.pop("extends_uuid", UNSET)

        extends_version = d.pop("extends_version", UNSET)

        published = d.pop("published", UNSET)

        deleted = d.pop("deleted", UNSET)

        galaxy_cluster_relation = []
        _galaxy_cluster_relation = d.pop("GalaxyClusterRelation", UNSET)
        for galaxy_cluster_relation_item_data in _galaxy_cluster_relation or []:
            galaxy_cluster_relation_item = AddEditGetEventGalaxyClusterRelation.from_dict(
                galaxy_cluster_relation_item_data
            )

            galaxy_cluster_relation.append(galaxy_cluster_relation_item)

        _org = d.pop("Org", UNSET)
        org: Union[Unset, Organisation]
        if isinstance(_org, Unset):
            org = UNSET
        else:
            org = Organisation.from_dict(_org)

        _orgc = d.pop("Orgc", UNSET)
        orgc: Union[Unset, Organisation]
        if isinstance(_orgc, Unset):
            orgc = UNSET
        else:
            orgc = Organisation.from_dict(_orgc)

        _meta = d.pop("meta", UNSET)
        meta: Union[Unset, AddEditGetEventGalaxyClusterMeta]
        if isinstance(_meta, Unset):
            meta = UNSET
        else:
            meta = AddEditGetEventGalaxyClusterMeta.from_dict(_meta)

        attribute_tag_id = d.pop("attribute_tag_id", UNSET)

        event_tag_id = d.pop("event_tag_id", UNSET)

        local = d.pop("local", UNSET)

        def _parse_relationship_type(data: object) -> Union[Unset, bool, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, bool, str], data)

        relationship_type = _parse_relationship_type(d.pop("relationship_type", UNSET))

        add_edit_get_event_galaxy_cluster = cls(
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
            tag_id=tag_id,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            default=default,
            locked=locked,
            extends_uuid=extends_uuid,
            extends_version=extends_version,
            published=published,
            deleted=deleted,
            galaxy_cluster_relation=galaxy_cluster_relation,
            org=org,
            orgc=orgc,
            meta=meta,
            attribute_tag_id=attribute_tag_id,
            event_tag_id=event_tag_id,
            local=local,
            relationship_type=relationship_type,
        )

        add_edit_get_event_galaxy_cluster.additional_properties = d
        return add_edit_get_event_galaxy_cluster

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
