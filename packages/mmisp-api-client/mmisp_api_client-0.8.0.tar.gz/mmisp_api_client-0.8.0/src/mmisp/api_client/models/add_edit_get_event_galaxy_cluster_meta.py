from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddEditGetEventGalaxyClusterMeta")


@_attrs_define
class AddEditGetEventGalaxyClusterMeta:
    """
    Attributes:
        external_id (Union[Unset, int]):
        refs (Union[Unset, list[str]]):
        kill_chain (Union[Unset, str]):
    """

    external_id: Union[Unset, int] = UNSET
    refs: Union[Unset, list[str]] = UNSET
    kill_chain: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        external_id = self.external_id

        refs: Union[Unset, list[str]] = UNSET
        if not isinstance(self.refs, Unset):
            refs = self.refs

        kill_chain = self.kill_chain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if refs is not UNSET:
            field_dict["refs"] = refs
        if kill_chain is not UNSET:
            field_dict["kill_chain"] = kill_chain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        external_id = d.pop("external_id", UNSET)

        refs = cast(list[str], d.pop("refs", UNSET))

        kill_chain = d.pop("kill_chain", UNSET)

        add_edit_get_event_galaxy_cluster_meta = cls(
            external_id=external_id,
            refs=refs,
            kill_chain=kill_chain,
        )

        add_edit_get_event_galaxy_cluster_meta.additional_properties = d
        return add_edit_get_event_galaxy_cluster_meta

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
