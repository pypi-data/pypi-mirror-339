from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.search_attributes_model_overrides_base_score_config import (
        SearchAttributesModelOverridesBaseScoreConfig,
    )


T = TypeVar("T", bound="SearchAttributesModelOverrides")


@_attrs_define
class SearchAttributesModelOverrides:
    """
    Attributes:
        lifetime (int):
        decay_speed (int):
        threshold (int):
        default_base_score (int):
        base_score_config (SearchAttributesModelOverridesBaseScoreConfig):
    """

    lifetime: int
    decay_speed: int
    threshold: int
    default_base_score: int
    base_score_config: "SearchAttributesModelOverridesBaseScoreConfig"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lifetime = self.lifetime

        decay_speed = self.decay_speed

        threshold = self.threshold

        default_base_score = self.default_base_score

        base_score_config = self.base_score_config.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "lifetime": lifetime,
                "decay_speed": decay_speed,
                "threshold": threshold,
                "default_base_score": default_base_score,
                "base_score_config": base_score_config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_attributes_model_overrides_base_score_config import (
            SearchAttributesModelOverridesBaseScoreConfig,
        )

        d = dict(src_dict)
        lifetime = d.pop("lifetime")

        decay_speed = d.pop("decay_speed")

        threshold = d.pop("threshold")

        default_base_score = d.pop("default_base_score")

        base_score_config = SearchAttributesModelOverridesBaseScoreConfig.from_dict(d.pop("base_score_config"))

        search_attributes_model_overrides = cls(
            lifetime=lifetime,
            decay_speed=decay_speed,
            threshold=threshold,
            default_base_score=default_base_score,
            base_score_config=base_score_config,
        )

        search_attributes_model_overrides.additional_properties = d
        return search_attributes_model_overrides

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
