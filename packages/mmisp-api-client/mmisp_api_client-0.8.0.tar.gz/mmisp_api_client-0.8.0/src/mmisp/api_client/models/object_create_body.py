from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.add_attribute_body import AddAttributeBody


T = TypeVar("T", bound="ObjectCreateBody")


@_attrs_define
class ObjectCreateBody:
    """
    Attributes:
        name (str):
        sharing_group_id (int):
        comment (str):
        meta_category (Union[Unset, str]):
        description (Union[Unset, str]):
        distribution (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        first_seen (Union[Unset, str]):
        last_seen (Union[Unset, str]):
        attribute (Union[Unset, list['AddAttributeBody']]):
    """

    name: str
    sharing_group_id: int
    comment: str
    meta_category: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    distribution: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    first_seen: Union[Unset, str] = UNSET
    last_seen: Union[Unset, str] = UNSET
    attribute: Union[Unset, list["AddAttributeBody"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        sharing_group_id = self.sharing_group_id

        comment = self.comment

        meta_category = self.meta_category

        description = self.description

        distribution = self.distribution

        deleted = self.deleted

        first_seen = self.first_seen

        last_seen = self.last_seen

        attribute: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attribute, Unset):
            attribute = []
            for attribute_item_data in self.attribute:
                attribute_item = attribute_item_data.to_dict()
                attribute.append(attribute_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "sharing_group_id": sharing_group_id,
                "comment": comment,
            }
        )
        if meta_category is not UNSET:
            field_dict["meta_category"] = meta_category
        if description is not UNSET:
            field_dict["description"] = description
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if first_seen is not UNSET:
            field_dict["first_seen"] = first_seen
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if attribute is not UNSET:
            field_dict["Attribute"] = attribute

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.add_attribute_body import AddAttributeBody

        d = dict(src_dict)
        name = d.pop("name")

        sharing_group_id = d.pop("sharing_group_id")

        comment = d.pop("comment")

        meta_category = d.pop("meta_category", UNSET)

        description = d.pop("description", UNSET)

        distribution = d.pop("distribution", UNSET)

        deleted = d.pop("deleted", UNSET)

        first_seen = d.pop("first_seen", UNSET)

        last_seen = d.pop("last_seen", UNSET)

        attribute = []
        _attribute = d.pop("Attribute", UNSET)
        for attribute_item_data in _attribute or []:
            attribute_item = AddAttributeBody.from_dict(attribute_item_data)

            attribute.append(attribute_item)

        object_create_body = cls(
            name=name,
            sharing_group_id=sharing_group_id,
            comment=comment,
            meta_category=meta_category,
            description=description,
            distribution=distribution,
            deleted=deleted,
            first_seen=first_seen,
            last_seen=last_seen,
            attribute=attribute,
        )

        object_create_body.additional_properties = d
        return object_create_body

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
