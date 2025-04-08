from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeedUpdateBody")


@_attrs_define
class FeedUpdateBody:
    """
    Attributes:
        name (Union[Unset, str]):
        provider (Union[Unset, str]):
        url (Union[Unset, str]):
        rules (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        distribution (Union[Unset, str]):
        sharing_group_id (Union[Unset, int]):
        tag_id (Union[Unset, int]):
        default (Union[Unset, bool]):
        source_format (Union[Unset, str]):
        fixed_event (Union[Unset, bool]):
        delta_merge (Union[Unset, bool]):
        event_id (Union[Unset, int]):
        publish (Union[Unset, bool]):
        override_ids (Union[Unset, bool]):
        settings (Union[Unset, str]):
        input_source (Union[Unset, str]):
        delete_local_file (Union[Unset, bool]):
        lookup_visible (Union[Unset, bool]):
        headers (Union[Unset, str]):
        caching_enabled (Union[Unset, bool]):
        force_to_ids (Union[Unset, bool]):
        orgc_id (Union[Unset, int]):
    """

    name: Union[Unset, str] = UNSET
    provider: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    rules: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    distribution: Union[Unset, str] = UNSET
    sharing_group_id: Union[Unset, int] = UNSET
    tag_id: Union[Unset, int] = UNSET
    default: Union[Unset, bool] = UNSET
    source_format: Union[Unset, str] = UNSET
    fixed_event: Union[Unset, bool] = UNSET
    delta_merge: Union[Unset, bool] = UNSET
    event_id: Union[Unset, int] = UNSET
    publish: Union[Unset, bool] = UNSET
    override_ids: Union[Unset, bool] = UNSET
    settings: Union[Unset, str] = UNSET
    input_source: Union[Unset, str] = UNSET
    delete_local_file: Union[Unset, bool] = UNSET
    lookup_visible: Union[Unset, bool] = UNSET
    headers: Union[Unset, str] = UNSET
    caching_enabled: Union[Unset, bool] = UNSET
    force_to_ids: Union[Unset, bool] = UNSET
    orgc_id: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        provider = self.provider

        url = self.url

        rules = self.rules

        enabled = self.enabled

        distribution = self.distribution

        sharing_group_id = self.sharing_group_id

        tag_id = self.tag_id

        default = self.default

        source_format = self.source_format

        fixed_event = self.fixed_event

        delta_merge = self.delta_merge

        event_id = self.event_id

        publish = self.publish

        override_ids = self.override_ids

        settings = self.settings

        input_source = self.input_source

        delete_local_file = self.delete_local_file

        lookup_visible = self.lookup_visible

        headers = self.headers

        caching_enabled = self.caching_enabled

        force_to_ids = self.force_to_ids

        orgc_id = self.orgc_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if provider is not UNSET:
            field_dict["provider"] = provider
        if url is not UNSET:
            field_dict["url"] = url
        if rules is not UNSET:
            field_dict["rules"] = rules
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if sharing_group_id is not UNSET:
            field_dict["sharing_group_id"] = sharing_group_id
        if tag_id is not UNSET:
            field_dict["tag_id"] = tag_id
        if default is not UNSET:
            field_dict["default"] = default
        if source_format is not UNSET:
            field_dict["source_format"] = source_format
        if fixed_event is not UNSET:
            field_dict["fixed_event"] = fixed_event
        if delta_merge is not UNSET:
            field_dict["delta_merge"] = delta_merge
        if event_id is not UNSET:
            field_dict["event_id"] = event_id
        if publish is not UNSET:
            field_dict["publish"] = publish
        if override_ids is not UNSET:
            field_dict["override_ids"] = override_ids
        if settings is not UNSET:
            field_dict["settings"] = settings
        if input_source is not UNSET:
            field_dict["input_source"] = input_source
        if delete_local_file is not UNSET:
            field_dict["delete_local_file"] = delete_local_file
        if lookup_visible is not UNSET:
            field_dict["lookup_visible"] = lookup_visible
        if headers is not UNSET:
            field_dict["headers"] = headers
        if caching_enabled is not UNSET:
            field_dict["caching_enabled"] = caching_enabled
        if force_to_ids is not UNSET:
            field_dict["force_to_ids"] = force_to_ids
        if orgc_id is not UNSET:
            field_dict["orgc_id"] = orgc_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        provider = d.pop("provider", UNSET)

        url = d.pop("url", UNSET)

        rules = d.pop("rules", UNSET)

        enabled = d.pop("enabled", UNSET)

        distribution = d.pop("distribution", UNSET)

        sharing_group_id = d.pop("sharing_group_id", UNSET)

        tag_id = d.pop("tag_id", UNSET)

        default = d.pop("default", UNSET)

        source_format = d.pop("source_format", UNSET)

        fixed_event = d.pop("fixed_event", UNSET)

        delta_merge = d.pop("delta_merge", UNSET)

        event_id = d.pop("event_id", UNSET)

        publish = d.pop("publish", UNSET)

        override_ids = d.pop("override_ids", UNSET)

        settings = d.pop("settings", UNSET)

        input_source = d.pop("input_source", UNSET)

        delete_local_file = d.pop("delete_local_file", UNSET)

        lookup_visible = d.pop("lookup_visible", UNSET)

        headers = d.pop("headers", UNSET)

        caching_enabled = d.pop("caching_enabled", UNSET)

        force_to_ids = d.pop("force_to_ids", UNSET)

        orgc_id = d.pop("orgc_id", UNSET)

        feed_update_body = cls(
            name=name,
            provider=provider,
            url=url,
            rules=rules,
            enabled=enabled,
            distribution=distribution,
            sharing_group_id=sharing_group_id,
            tag_id=tag_id,
            default=default,
            source_format=source_format,
            fixed_event=fixed_event,
            delta_merge=delta_merge,
            event_id=event_id,
            publish=publish,
            override_ids=override_ids,
            settings=settings,
            input_source=input_source,
            delete_local_file=delete_local_file,
            lookup_visible=lookup_visible,
            headers=headers,
            caching_enabled=caching_enabled,
            force_to_ids=force_to_ids,
            orgc_id=orgc_id,
        )

        feed_update_body.additional_properties = d
        return feed_update_body

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
