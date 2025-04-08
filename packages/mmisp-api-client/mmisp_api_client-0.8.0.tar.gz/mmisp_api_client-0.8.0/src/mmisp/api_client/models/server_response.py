from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServerResponse")


@_attrs_define
class ServerResponse:
    """
    Attributes:
        id (int):
        name (str):
        url (str):
        push (bool):
        pull (bool):
        organization (None):
        pull_analyst_data (bool):
        pull_rules (str):
        push_analyst_data (bool):
        push_rules (str):
        remove_missing_tags (bool):
        remote_org_id (int):
        self_signed (bool):
        org_id (Union[Unset, int]):
        cert_file (Union[Unset, str]):
        client_cert_file (Union[Unset, str]):
        lastpulledid (Union[Unset, int]):
        lastpushedid (Union[Unset, int]):
        push_sightings (Union[Unset, bool]):
        push_galaxy_clusters (Union[Unset, bool]):
        pull_galaxy_clusters (Union[Unset, bool]):
        publish_without_email (Union[Unset, bool]):
        unpublish_event (Union[Unset, bool]):
        internal (Union[Unset, bool]):
        skip_proxy (Union[Unset, bool]):
        caching_enabled (Union[Unset, bool]):
        priority (Union[Unset, int]):
        cache_timestamp (Union[Unset, bool]):  Default: False.
    """

    id: int
    name: str
    url: str
    push: bool
    pull: bool
    organization: None
    pull_analyst_data: bool
    pull_rules: str
    push_analyst_data: bool
    push_rules: str
    remove_missing_tags: bool
    remote_org_id: int
    self_signed: bool
    org_id: Union[Unset, int] = UNSET
    cert_file: Union[Unset, str] = UNSET
    client_cert_file: Union[Unset, str] = UNSET
    lastpulledid: Union[Unset, int] = UNSET
    lastpushedid: Union[Unset, int] = UNSET
    push_sightings: Union[Unset, bool] = UNSET
    push_galaxy_clusters: Union[Unset, bool] = UNSET
    pull_galaxy_clusters: Union[Unset, bool] = UNSET
    publish_without_email: Union[Unset, bool] = UNSET
    unpublish_event: Union[Unset, bool] = UNSET
    internal: Union[Unset, bool] = UNSET
    skip_proxy: Union[Unset, bool] = UNSET
    caching_enabled: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    cache_timestamp: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        url = self.url

        push = self.push

        pull = self.pull

        organization = self.organization

        pull_analyst_data = self.pull_analyst_data

        pull_rules = self.pull_rules

        push_analyst_data = self.push_analyst_data

        push_rules = self.push_rules

        remove_missing_tags = self.remove_missing_tags

        remote_org_id = self.remote_org_id

        self_signed = self.self_signed

        org_id = self.org_id

        cert_file = self.cert_file

        client_cert_file = self.client_cert_file

        lastpulledid = self.lastpulledid

        lastpushedid = self.lastpushedid

        push_sightings = self.push_sightings

        push_galaxy_clusters = self.push_galaxy_clusters

        pull_galaxy_clusters = self.pull_galaxy_clusters

        publish_without_email = self.publish_without_email

        unpublish_event = self.unpublish_event

        internal = self.internal

        skip_proxy = self.skip_proxy

        caching_enabled = self.caching_enabled

        priority = self.priority

        cache_timestamp = self.cache_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "url": url,
                "push": push,
                "pull": pull,
                "organization": organization,
                "pull_analyst_data": pull_analyst_data,
                "pull_rules": pull_rules,
                "push_analyst_data": push_analyst_data,
                "push_rules": push_rules,
                "remove_missing_tags": remove_missing_tags,
                "remote_org_id": remote_org_id,
                "self_signed": self_signed,
            }
        )
        if org_id is not UNSET:
            field_dict["org_id"] = org_id
        if cert_file is not UNSET:
            field_dict["cert_file"] = cert_file
        if client_cert_file is not UNSET:
            field_dict["client_cert_file"] = client_cert_file
        if lastpulledid is not UNSET:
            field_dict["lastpulledid"] = lastpulledid
        if lastpushedid is not UNSET:
            field_dict["lastpushedid"] = lastpushedid
        if push_sightings is not UNSET:
            field_dict["push_sightings"] = push_sightings
        if push_galaxy_clusters is not UNSET:
            field_dict["push_galaxy_clusters"] = push_galaxy_clusters
        if pull_galaxy_clusters is not UNSET:
            field_dict["pull_galaxy_clusters"] = pull_galaxy_clusters
        if publish_without_email is not UNSET:
            field_dict["publish_without_email"] = publish_without_email
        if unpublish_event is not UNSET:
            field_dict["unpublish_event"] = unpublish_event
        if internal is not UNSET:
            field_dict["internal"] = internal
        if skip_proxy is not UNSET:
            field_dict["skip_proxy"] = skip_proxy
        if caching_enabled is not UNSET:
            field_dict["caching_enabled"] = caching_enabled
        if priority is not UNSET:
            field_dict["priority"] = priority
        if cache_timestamp is not UNSET:
            field_dict["cache_timestamp"] = cache_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        url = d.pop("url")

        push = d.pop("push")

        pull = d.pop("pull")

        organization = d.pop("organization")

        pull_analyst_data = d.pop("pull_analyst_data")

        pull_rules = d.pop("pull_rules")

        push_analyst_data = d.pop("push_analyst_data")

        push_rules = d.pop("push_rules")

        remove_missing_tags = d.pop("remove_missing_tags")

        remote_org_id = d.pop("remote_org_id")

        self_signed = d.pop("self_signed")

        org_id = d.pop("org_id", UNSET)

        cert_file = d.pop("cert_file", UNSET)

        client_cert_file = d.pop("client_cert_file", UNSET)

        lastpulledid = d.pop("lastpulledid", UNSET)

        lastpushedid = d.pop("lastpushedid", UNSET)

        push_sightings = d.pop("push_sightings", UNSET)

        push_galaxy_clusters = d.pop("push_galaxy_clusters", UNSET)

        pull_galaxy_clusters = d.pop("pull_galaxy_clusters", UNSET)

        publish_without_email = d.pop("publish_without_email", UNSET)

        unpublish_event = d.pop("unpublish_event", UNSET)

        internal = d.pop("internal", UNSET)

        skip_proxy = d.pop("skip_proxy", UNSET)

        caching_enabled = d.pop("caching_enabled", UNSET)

        priority = d.pop("priority", UNSET)

        cache_timestamp = d.pop("cache_timestamp", UNSET)

        server_response = cls(
            id=id,
            name=name,
            url=url,
            push=push,
            pull=pull,
            organization=organization,
            pull_analyst_data=pull_analyst_data,
            pull_rules=pull_rules,
            push_analyst_data=push_analyst_data,
            push_rules=push_rules,
            remove_missing_tags=remove_missing_tags,
            remote_org_id=remote_org_id,
            self_signed=self_signed,
            org_id=org_id,
            cert_file=cert_file,
            client_cert_file=client_cert_file,
            lastpulledid=lastpulledid,
            lastpushedid=lastpushedid,
            push_sightings=push_sightings,
            push_galaxy_clusters=push_galaxy_clusters,
            pull_galaxy_clusters=pull_galaxy_clusters,
            publish_without_email=publish_without_email,
            unpublish_event=unpublish_event,
            internal=internal,
            skip_proxy=skip_proxy,
            caching_enabled=caching_enabled,
            priority=priority,
            cache_timestamp=cache_timestamp,
        )

        server_response.additional_properties = d
        return server_response

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
