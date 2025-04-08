from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feed_attributes_response import FeedAttributesResponse


T = TypeVar("T", bound="FeedResponse")


@_attrs_define
class FeedResponse:
    """
    Attributes:
        feed (FeedAttributesResponse):
    """

    feed: "FeedAttributesResponse"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        feed = self.feed.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Feed": feed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feed_attributes_response import FeedAttributesResponse

        d = dict(src_dict)
        feed = FeedAttributesResponse.from_dict(d.pop("Feed"))

        feed_response = cls(
            feed=feed,
        )

        feed_response.additional_properties = d
        return feed_response

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
