from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Data")


@_attrs_define
class Data:
    """
    Attributes:
        scope (Union[Unset, list[str], str]):
        field (Union[Unset, list[str], str]):
        value (Union[Unset, list[str], str]):
        tags (Union[Unset, list[str], str]):
        message (Union[Any, Unset, str]):
    """

    scope: Union[Unset, list[str], str] = UNSET
    field: Union[Unset, list[str], str] = UNSET
    value: Union[Unset, list[str], str] = UNSET
    tags: Union[Unset, list[str], str] = UNSET
    message: Union[Any, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope: Union[Unset, list[str], str]
        if isinstance(self.scope, Unset):
            scope = UNSET
        elif isinstance(self.scope, list):
            scope = self.scope

        else:
            scope = self.scope

        field: Union[Unset, list[str], str]
        if isinstance(self.field, Unset):
            field = UNSET
        elif isinstance(self.field, list):
            field = self.field

        else:
            field = self.field

        value: Union[Unset, list[str], str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        tags: Union[Unset, list[str], str]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        message: Union[Any, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scope is not UNSET:
            field_dict["scope"] = scope
        if field is not UNSET:
            field_dict["field"] = field
        if value is not UNSET:
            field_dict["value"] = value
        if tags is not UNSET:
            field_dict["tags"] = tags
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_scope(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scope_type_1 = cast(list[str], data)

                return scope_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        scope = _parse_scope(d.pop("scope", UNSET))

        def _parse_field(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                field_type_1 = cast(list[str], data)

                return field_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        field = _parse_field(d.pop("field", UNSET))

        def _parse_value(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_tags(data: object) -> Union[Unset, list[str], str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_1 = cast(list[str], data)

                return tags_type_1
            except:  # noqa: E722
                pass
            return cast(Union[Unset, list[str], str], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_message(data: object) -> Union[Any, Unset, str]:
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        data = cls(
            scope=scope,
            field=field,
            value=value,
            tags=tags,
            message=message,
        )

        data.additional_properties = d
        return data

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
