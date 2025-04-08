from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_edit_get_event_galaxy_cluster_relation_tag import AddEditGetEventGalaxyClusterRelationTag


T = TypeVar("T", bound="AddEditGetEventGalaxyClusterRelation")


@_attrs_define
class AddEditGetEventGalaxyClusterRelation:
    """
    Attributes:
        id (int):
        galaxy_cluster_id (int):
        referenced_galaxy_cluster_id (int):
        referenced_galaxy_cluster_uuid (str):
        referenced_galaxy_cluster_type (str):
        galaxy_cluster_uuid (str):
        distribution (str):
        default (bool):
        sharing_group_id (Union[Unset, int]):
        tag (Union[Unset, list['AddEditGetEventGalaxyClusterRelationTag']]):
    """

    id: int
    galaxy_cluster_id: int
    referenced_galaxy_cluster_id: int
    referenced_galaxy_cluster_uuid: str
    referenced_galaxy_cluster_type: str
    galaxy_cluster_uuid: str
    distribution: str
    default: bool
    sharing_group_id: Union[Unset, int] = UNSET
    tag: Union[Unset, list["AddEditGetEventGalaxyClusterRelationTag"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        galaxy_cluster_id = self.galaxy_cluster_id

        referenced_galaxy_cluster_id = self.referenced_galaxy_cluster_id

        referenced_galaxy_cluster_uuid = self.referenced_galaxy_cluster_uuid

        referenced_galaxy_cluster_type = self.referenced_galaxy_cluster_type

        galaxy_cluster_uuid = self.galaxy_cluster_uuid

        distribution = self.distribution

        default = self.default

        sharing_group_id = self.sharing_group_id

        tag: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tag, Unset):
            tag = []
            for tag_item_data in self.tag:
                tag_item = tag_item_data.to_dict()
                tag.append(tag_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "galaxy_cluster_id": galaxy_cluster_id,
                "referenced_galaxy_cluster_id": referenced_galaxy_cluster_id,
                "referenced_galaxy_cluster_uuid": referenced_galaxy_cluster_uuid,
                "referenced_galaxy_cluster_type": referenced_galaxy_cluster_type,
                "galaxy_cluster_uuid": galaxy_cluster_uuid,
                "distribution": distribution,
                "default": default,
            }
        )
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if tag is not UNSET:
            field_dict["Tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_edit_get_event_galaxy_cluster_relation_tag import AddEditGetEventGalaxyClusterRelationTag

        d = dict(src_dict)
        id = d.pop("id")

        galaxy_cluster_id = d.pop("galaxy_cluster_id")

        referenced_galaxy_cluster_id = d.pop("referenced_galaxy_cluster_id")

        referenced_galaxy_cluster_uuid = d.pop("referenced_galaxy_cluster_uuid")

        referenced_galaxy_cluster_type = d.pop("referenced_galaxy_cluster_type")

        galaxy_cluster_uuid = d.pop("galaxy_cluster_uuid")

        distribution = d.pop("distribution")

        default = d.pop("default")

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        tag = []
        _tag = d.pop("Tag", UNSET)
        for tag_item_data in _tag or []:
            tag_item = AddEditGetEventGalaxyClusterRelationTag.from_dict(tag_item_data)

            tag.append(tag_item)

        add_edit_get_event_galaxy_cluster_relation = cls(
            id=id,
            galaxy_cluster_id=galaxy_cluster_id,
            referenced_galaxy_cluster_id=referenced_galaxy_cluster_id,
            referenced_galaxy_cluster_uuid=referenced_galaxy_cluster_uuid,
            referenced_galaxy_cluster_type=referenced_galaxy_cluster_type,
            galaxy_cluster_uuid=galaxy_cluster_uuid,
            distribution=distribution,
            default=default,
            sharing_group_id=sharing_group_id,
            tag=tag,
        )

        add_edit_get_event_galaxy_cluster_relation.additional_properties = d
        return add_edit_get_event_galaxy_cluster_relation

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
