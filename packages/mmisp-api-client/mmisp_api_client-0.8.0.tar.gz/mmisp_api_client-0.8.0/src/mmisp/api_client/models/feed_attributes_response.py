from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeedAttributesResponse")


@_attrs_define
class FeedAttributesResponse:
    """
    Attributes:
        id (int):
        name (str):
        provider (str):
        url (str):
        distribution (str):
        tag_id (int):
        fixed_event (bool):
        delta_merge (bool):
        event_id (int):
        publish (bool):
        override_ids (bool):
        input_source (str):
        caching_enabled (bool):
        force_to_ids (bool):
        orgc_id (int):
        rules (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        sharing_group_id (Union[Unset, int]):
        default (Union[Unset, bool]):
        source_format (Union[Unset, str]):
        settings (Union[Unset, str]):
        delete_local_file (Union[Unset, bool]):
        lookup_visible (Union[Unset, bool]):
        headers (Union[Unset, str]):
    """

    id: int
    name: str
    provider: str
    url: str
    distribution: str
    tag_id: int
    fixed_event: bool
    delta_merge: bool
    event_id: int
    publish: bool
    override_ids: bool
    input_source: str
    caching_enabled: bool
    force_to_ids: bool
    orgc_id: int
    rules: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    default: Union[Unset, bool] = UNSET
    source_format: Union[Unset, str] = UNSET
    settings: Union[Unset, str] = UNSET
    delete_local_file: Union[Unset, bool] = UNSET
    lookup_visible: Union[Unset, bool] = UNSET
    headers: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        provider = self.provider

        url = self.url

        distribution = self.distribution

        tag_id = self.tag_id

        fixed_event = self.fixed_event

        delta_merge = self.delta_merge

        event_id = self.event_id

        publish = self.publish

        override_ids = self.override_ids

        input_source = self.input_source

        caching_enabled = self.caching_enabled

        force_to_ids = self.force_to_ids

        orgc_id = self.orgc_id

        rules = self.rules

        enabled = self.enabled

        sharing_group_id = self.sharing_group_id

        default = self.default

        source_format = self.source_format

        settings = self.settings

        delete_local_file = self.delete_local_file

        lookup_visible = self.lookup_visible

        headers = self.headers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "provider": provider,
                "url": url,
                "distribution": distribution,
                "tag_id": tag_id,
                "fixed_event": fixed_event,
                "delta_merge": delta_merge,
                "event_id": event_id,
                "publish": publish,
                "override_ids": override_ids,
                "input_source": input_source,
                "caching_enabled": caching_enabled,
                "force_to_ids": force_to_ids,
                "orgc_id": orgc_id,
            }
        )
        if rules is not UNSET:
            field_dict["rules"] = rules
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if default is not UNSET:
            field_dict["default"] = default
        if source_format is not UNSET:
            field_dict["source_format"] = source_format
        if settings is not UNSET:
            field_dict["settings"] = settings
        if delete_local_file is not UNSET:
            field_dict["delete_local_file"] = delete_local_file
        if lookup_visible is not UNSET:
            field_dict["lookup_visible"] = lookup_visible
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        provider = d.pop("provider")

        url = d.pop("url")

        distribution = d.pop("distribution")

        tag_id = d.pop("tag_id")

        fixed_event = d.pop("fixed_event")

        delta_merge = d.pop("delta_merge")

        event_id = d.pop("event_id")

        publish = d.pop("publish")

        override_ids = d.pop("override_ids")

        input_source = d.pop("input_source")

        caching_enabled = d.pop("caching_enabled")

        force_to_ids = d.pop("force_to_ids")

        orgc_id = d.pop("orgc_id")

        rules = d.pop("rules", UNSET)

        enabled = d.pop("enabled", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        default = d.pop("default", UNSET)

        source_format = d.pop("source_format", UNSET)

        settings = d.pop("settings", UNSET)

        delete_local_file = d.pop("delete_local_file", UNSET)

        lookup_visible = d.pop("lookup_visible", UNSET)

        headers = d.pop("headers", UNSET)

        feed_attributes_response = cls(
            id=id,
            name=name,
            provider=provider,
            url=url,
            distribution=distribution,
            tag_id=tag_id,
            fixed_event=fixed_event,
            delta_merge=delta_merge,
            event_id=event_id,
            publish=publish,
            override_ids=override_ids,
            input_source=input_source,
            caching_enabled=caching_enabled,
            force_to_ids=force_to_ids,
            orgc_id=orgc_id,
            rules=rules,
            enabled=enabled,
            sharing_group_id=sharing_group_id,
            default=default,
            source_format=source_format,
            settings=settings,
            delete_local_file=delete_local_file,
            lookup_visible=lookup_visible,
            headers=headers,
        )

        feed_attributes_response.additional_properties = d
        return feed_attributes_response

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
