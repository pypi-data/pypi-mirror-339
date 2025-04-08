import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleAttributeResponse")


@_attrs_define
class RoleAttributeResponse:
    """
    Attributes:
        id (int):
        name (str):
        default_role (bool):
        restricted_to_site_admin (bool):
        enforce_rate_limit (bool):
        rate_limit_count (int):
        perm_add (Union[Unset, bool]):
        perm_modify (Union[Unset, bool]):
        perm_modify_org (Union[Unset, bool]):
        perm_publish (Union[Unset, bool]):
        perm_delegate (Union[Unset, bool]):
        perm_sync (Union[Unset, bool]):
        perm_admin (Union[Unset, bool]):
        perm_audit (Union[Unset, bool]):
        perm_auth (Union[Unset, bool]):
        perm_site_admin (Union[Unset, bool]):
        perm_regexp_access (Union[Unset, bool]):
        perm_tagger (Union[Unset, bool]):
        perm_template (Union[Unset, bool]):
        perm_sharing_group (Union[Unset, bool]):
        perm_tag_editor (Union[Unset, bool]):
        perm_sighting (Union[Unset, bool]):
        perm_object_template (Union[Unset, bool]):
        perm_publish_zmq (Union[Unset, bool]):
        perm_publish_kafka (Union[Unset, bool]):
        perm_decaying (Union[Unset, bool]):
        perm_galaxy_editor (Union[Unset, bool]):
        perm_warninglist (Union[Unset, bool]):
        perm_view_feed_correlations (Union[Unset, bool]):
        perm_skip_otp (Union[Unset, bool]):
        perm_server_sign (Union[Unset, bool]):
        perm_analyst_data (Union[Unset, bool]):
        perm_sync_authoritative (Union[Unset, bool]):
        perm_sync_internal (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime, str]):
        modified (Union[Unset, datetime.datetime, str]):
        memory_limit (Union[Unset, str]):
        max_execution_time (Union[Unset, str]):
        permission (Union[Unset, int]):
        permission_description (Union[Unset, str]):
        default (Union[Unset, bool]):  Default: False.
    """

    id: int
    name: str
    default_role: bool
    restricted_to_site_admin: bool
    enforce_rate_limit: bool
    rate_limit_count: int
    perm_add: Union[Unset, bool] = UNSET
    perm_modify: Union[Unset, bool] = UNSET
    perm_modify_org: Union[Unset, bool] = UNSET
    perm_publish: Union[Unset, bool] = UNSET
    perm_delegate: Union[Unset, bool] = UNSET
    perm_sync: Union[Unset, bool] = UNSET
    perm_admin: Union[Unset, bool] = UNSET
    perm_audit: Union[Unset, bool] = UNSET
    perm_auth: Union[Unset, bool] = UNSET
    perm_site_admin: Union[Unset, bool] = UNSET
    perm_regexp_access: Union[Unset, bool] = UNSET
    perm_tagger: Union[Unset, bool] = UNSET
    perm_template: Union[Unset, bool] = UNSET
    perm_sharing_group: Union[Unset, bool] = UNSET
    perm_tag_editor: Union[Unset, bool] = UNSET
    perm_sighting: Union[Unset, bool] = UNSET
    perm_object_template: Union[Unset, bool] = UNSET
    perm_publish_zmq: Union[Unset, bool] = UNSET
    perm_publish_kafka: Union[Unset, bool] = UNSET
    perm_decaying: Union[Unset, bool] = UNSET
    perm_galaxy_editor: Union[Unset, bool] = UNSET
    perm_warninglist: Union[Unset, bool] = UNSET
    perm_view_feed_correlations: Union[Unset, bool] = UNSET
    perm_skip_otp: Union[Unset, bool] = UNSET
    perm_server_sign: Union[Unset, bool] = UNSET
    perm_analyst_data: Union[Unset, bool] = UNSET
    perm_sync_authoritative: Union[Unset, bool] = UNSET
    perm_sync_internal: Union[Unset, bool] = UNSET
    created: Union[Unset, datetime.datetime, str] = UNSET
    modified: Union[Unset, datetime.datetime, str] = UNSET
    memory_limit: Union[Unset, str] = UNSET
    max_execution_time: Union[Unset, str] = UNSET
    permission: Union[Unset, int] = UNSET
    permission_description: Union[Unset, str] = UNSET
    default: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        default_role = self.default_role

        restricted_to_site_admin = self.restricted_to_site_admin

        enforce_rate_limit = self.enforce_rate_limit

        rate_limit_count = self.rate_limit_count

        perm_add = self.perm_add

        perm_modify = self.perm_modify

        perm_modify_org = self.perm_modify_org

        perm_publish = self.perm_publish

        perm_delegate = self.perm_delegate

        perm_sync = self.perm_sync

        perm_admin = self.perm_admin

        perm_audit = self.perm_audit

        perm_auth = self.perm_auth

        perm_site_admin = self.perm_site_admin

        perm_regexp_access = self.perm_regexp_access

        perm_tagger = self.perm_tagger

        perm_template = self.perm_template

        perm_sharing_group = self.perm_sharing_group

        perm_tag_editor = self.perm_tag_editor

        perm_sighting = self.perm_sighting

        perm_object_template = self.perm_object_template

        perm_publish_zmq = self.perm_publish_zmq

        perm_publish_kafka = self.perm_publish_kafka

        perm_decaying = self.perm_decaying

        perm_galaxy_editor = self.perm_galaxy_editor

        perm_warninglist = self.perm_warninglist

        perm_view_feed_correlations = self.perm_view_feed_correlations

        perm_skip_otp = self.perm_skip_otp

        perm_server_sign = self.perm_server_sign

        perm_analyst_data = self.perm_analyst_data

        perm_sync_authoritative = self.perm_sync_authoritative

        perm_sync_internal = self.perm_sync_internal

        created: Union[Unset, str]
        if isinstance(self.created, Unset):
            created = UNSET
        elif isinstance(self.created, datetime.datetime):
            created = self.created.isoformat()
        else:
            created = self.created

        modified: Union[Unset, str]
        if isinstance(self.modified, Unset):
            modified = UNSET
        elif isinstance(self.modified, datetime.datetime):
            modified = self.modified.isoformat()
        else:
            modified = self.modified

        memory_limit = self.memory_limit

        max_execution_time = self.max_execution_time

        permission = self.permission

        permission_description = self.permission_description

        default = self.default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "default_role": default_role,
                "restricted_to_site_admin": restricted_to_site_admin,
                "enforce_rate_limit": enforce_rate_limit,
                "rate_limit_count": rate_limit_count,
            }
        )
        if perm_add is not UNSET:
            field_dict["perm_add"] = perm_add
        if perm_modify is not UNSET:
            field_dict["perm_modify"] = perm_modify
        if perm_modify_org is not UNSET:
            field_dict["perm_modify_org"] = perm_modify_org
        if perm_publish is not UNSET:
            field_dict["perm_publish"] = perm_publish
        if perm_delegate is not UNSET:
            field_dict["perm_delegate"] = perm_delegate
        if perm_sync is not UNSET:
            field_dict["perm_sync"] = perm_sync
        if perm_admin is not UNSET:
            field_dict["perm_admin"] = perm_admin
        if perm_audit is not UNSET:
            field_dict["perm_audit"] = perm_audit
        if perm_auth is not UNSET:
            field_dict["perm_auth"] = perm_auth
        if perm_site_admin is not UNSET:
            field_dict["perm_site_admin"] = perm_site_admin
        if perm_regexp_access is not UNSET:
            field_dict["perm_regexp_access"] = perm_regexp_access
        if perm_tagger is not UNSET:
            field_dict["perm_tagger"] = perm_tagger
        if perm_template is not UNSET:
            field_dict["perm_template"] = perm_template
        if perm_sharing_group is not UNSET:
            field_dict["perm_sharing_group"] = perm_sharing_group
        if perm_tag_editor is not UNSET:
            field_dict["perm_tag_editor"] = perm_tag_editor
        if perm_sighting is not UNSET:
            field_dict["perm_sighting"] = perm_sighting
        if perm_object_template is not UNSET:
            field_dict["perm_object_template"] = perm_object_template
        if perm_publish_zmq is not UNSET:
            field_dict["perm_publish_zmq"] = perm_publish_zmq
        if perm_publish_kafka is not UNSET:
            field_dict["perm_publish_kafka"] = perm_publish_kafka
        if perm_decaying is not UNSET:
            field_dict["perm_decaying"] = perm_decaying
        if perm_galaxy_editor is not UNSET:
            field_dict["perm_galaxy_editor"] = perm_galaxy_editor
        if perm_warninglist is not UNSET:
            field_dict["perm_warninglist"] = perm_warninglist
        if perm_view_feed_correlations is not UNSET:
            field_dict["perm_view_feed_correlations"] = perm_view_feed_correlations
        if perm_skip_otp is not UNSET:
            field_dict["perm_skip_otp"] = perm_skip_otp
        if perm_server_sign is not UNSET:
            field_dict["perm_server_sign"] = perm_server_sign
        if perm_analyst_data is not UNSET:
            field_dict["perm_analyst_data"] = perm_analyst_data
        if perm_sync_authoritative is not UNSET:
            field_dict["perm_sync_authoritative"] = perm_sync_authoritative
        if perm_sync_internal is not UNSET:
            field_dict["perm_sync_internal"] = perm_sync_internal
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if memory_limit is not UNSET:
            field_dict["memory_limit"] = memory_limit
        if max_execution_time is not UNSET:
            field_dict["max_execution_time"] = max_execution_time
        if permission is not UNSET:
            field_dict["permission"] = permission
        if permission_description is not UNSET:
            field_dict["permission_description"] = permission_description
        if default is not UNSET:
            field_dict["default"] = default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        default_role = d.pop("default_role")

        restricted_to_site_admin = d.pop("restricted_to_site_admin")

        enforce_rate_limit = d.pop("enforce_rate_limit")

        rate_limit_count = d.pop("rate_limit_count")

        perm_add = d.pop("perm_add", UNSET)

        perm_modify = d.pop("perm_modify", UNSET)

        perm_modify_org = d.pop("perm_modify_org", UNSET)

        perm_publish = d.pop("perm_publish", UNSET)

        perm_delegate = d.pop("perm_delegate", UNSET)

        perm_sync = d.pop("perm_sync", UNSET)

        perm_admin = d.pop("perm_admin", UNSET)

        perm_audit = d.pop("perm_audit", UNSET)

        perm_auth = d.pop("perm_auth", UNSET)

        perm_site_admin = d.pop("perm_site_admin", UNSET)

        perm_regexp_access = d.pop("perm_regexp_access", UNSET)

        perm_tagger = d.pop("perm_tagger", UNSET)

        perm_template = d.pop("perm_template", UNSET)

        perm_sharing_group = d.pop("perm_sharing_group", UNSET)

        perm_tag_editor = d.pop("perm_tag_editor", UNSET)

        perm_sighting = d.pop("perm_sighting", UNSET)

        perm_object_template = d.pop("perm_object_template", UNSET)

        perm_publish_zmq = d.pop("perm_publish_zmq", UNSET)

        perm_publish_kafka = d.pop("perm_publish_kafka", UNSET)

        perm_decaying = d.pop("perm_decaying", UNSET)

        perm_galaxy_editor = d.pop("perm_galaxy_editor", UNSET)

        perm_warninglist = d.pop("perm_warninglist", UNSET)

        perm_view_feed_correlations = d.pop("perm_view_feed_correlations", UNSET)

        perm_skip_otp = d.pop("perm_skip_otp", UNSET)

        perm_server_sign = d.pop("perm_server_sign", UNSET)

        perm_analyst_data = d.pop("perm_analyst_data", UNSET)

        perm_sync_authoritative = d.pop("perm_sync_authoritative", UNSET)

        perm_sync_internal = d.pop("perm_sync_internal", UNSET)

        def _parse_created(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_type_0 = isoparse(data)

                return created_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        created = _parse_created(d.pop("created", UNSET))

        def _parse_modified(data: object) -> Union[Unset, datetime.datetime, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                modified_type_0 = isoparse(data)

                return modified_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, str], data)

        modified = _parse_modified(d.pop("modified", UNSET))

        memory_limit = d.pop("memory_limit", UNSET)

        max_execution_time = d.pop("max_execution_time", UNSET)

        permission = d.pop("permission", UNSET)

        permission_description = d.pop("permission_description", UNSET)

        default = d.pop("default", UNSET)

        role_attribute_response = cls(
            id=id,
            name=name,
            default_role=default_role,
            restricted_to_site_admin=restricted_to_site_admin,
            enforce_rate_limit=enforce_rate_limit,
            rate_limit_count=rate_limit_count,
            perm_add=perm_add,
            perm_modify=perm_modify,
            perm_modify_org=perm_modify_org,
            perm_publish=perm_publish,
            perm_delegate=perm_delegate,
            perm_sync=perm_sync,
            perm_admin=perm_admin,
            perm_audit=perm_audit,
            perm_auth=perm_auth,
            perm_site_admin=perm_site_admin,
            perm_regexp_access=perm_regexp_access,
            perm_tagger=perm_tagger,
            perm_template=perm_template,
            perm_sharing_group=perm_sharing_group,
            perm_tag_editor=perm_tag_editor,
            perm_sighting=perm_sighting,
            perm_object_template=perm_object_template,
            perm_publish_zmq=perm_publish_zmq,
            perm_publish_kafka=perm_publish_kafka,
            perm_decaying=perm_decaying,
            perm_galaxy_editor=perm_galaxy_editor,
            perm_warninglist=perm_warninglist,
            perm_view_feed_correlations=perm_view_feed_correlations,
            perm_skip_otp=perm_skip_otp,
            perm_server_sign=perm_server_sign,
            perm_analyst_data=perm_analyst_data,
            perm_sync_authoritative=perm_sync_authoritative,
            perm_sync_internal=perm_sync_internal,
            created=created,
            modified=modified,
            memory_limit=memory_limit,
            max_execution_time=max_execution_time,
            permission=permission,
            permission_description=permission_description,
            default=default,
        )

        role_attribute_response.additional_properties = d
        return role_attribute_response

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
