from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogsRequest")


@_attrs_define
class LogsRequest:
    """
    Attributes:
        model (Union[Unset, str]):
        action (Union[Unset, str]):
        model_id (Union[Unset, int]):
        page (Union[Unset, int]):  Default: 1.
        limit (Union[Unset, int]):  Default: 50.
    """

    model: Union[Unset, str] = UNSET
    action: Union[Unset, str] = UNSET
    model_id: Union[Unset, int] = UNSET
    page: Union[Unset, int] = 1
    limit: Union[Unset, int] = 50
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        action = self.action

        model_id = self.model_id

        page = self.page

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model is not UNSET:
            field_dict["model"] = model
        if action is not UNSET:
            field_dict["action"] = action
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if page is not UNSET:
            field_dict["page"] = page
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model", UNSET)

        action = d.pop("action", UNSET)

        model_id = d.pop("model_id", UNSET)

        page = d.pop("page", UNSET)

        limit = d.pop("limit", UNSET)

        logs_request = cls(
            model=model,
            action=action,
            model_id=model_id,
            page=page,
            limit=limit,
        )

        logs_request.additional_properties = d
        return logs_request

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
