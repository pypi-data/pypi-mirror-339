from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.not_filter import NOTFilter
    from ..models.ornot_filter import ORNOTFilter


T = TypeVar("T", bound="PullRulesFilter")


@_attrs_define
class PullRulesFilter:
    """
    Attributes:
        tags (ORNOTFilter):
        orgs (ORNOTFilter):
        type_attributes (NOTFilter):
        type_objects (NOTFilter):
        url_params (str):
    """

    tags: "ORNOTFilter"
    orgs: "ORNOTFilter"
    type_attributes: "NOTFilter"
    type_objects: "NOTFilter"
    url_params: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tags = self.tags.to_dict()

        orgs = self.orgs.to_dict()

        type_attributes = self.type_attributes.to_dict()

        type_objects = self.type_objects.to_dict()

        url_params = self.url_params

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tags": tags,
                "orgs": orgs,
                "type_attributes": type_attributes,
                "type_objects": type_objects,
                "url_params": url_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.not_filter import NOTFilter
        from ..models.ornot_filter import ORNOTFilter

        d = dict(src_dict)
        tags = ORNOTFilter.from_dict(d.pop("tags"))

        orgs = ORNOTFilter.from_dict(d.pop("orgs"))

        type_attributes = NOTFilter.from_dict(d.pop("type_attributes"))

        type_objects = NOTFilter.from_dict(d.pop("type_objects"))

        url_params = d.pop("url_params")

        pull_rules_filter = cls(
            tags=tags,
            orgs=orgs,
            type_attributes=type_attributes,
            type_objects=type_objects,
            url_params=url_params,
        )

        pull_rules_filter.additional_properties = d
        return pull_rules_filter

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
