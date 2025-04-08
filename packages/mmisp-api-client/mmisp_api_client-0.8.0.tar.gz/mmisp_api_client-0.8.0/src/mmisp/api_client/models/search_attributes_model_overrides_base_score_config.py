from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchAttributesModelOverridesBaseScoreConfig")


@_attrs_define
class SearchAttributesModelOverridesBaseScoreConfig:
    """
    Attributes:
        estimative_languageconfidence_in_analytic_judgment (int):
        estimative_languagelikelihood_probability (int):
        phishingpsychological_acceptability (int):
        phishingstate (int):
    """

    estimative_languageconfidence_in_analytic_judgment: int
    estimative_languagelikelihood_probability: int
    phishingpsychological_acceptability: int
    phishingstate: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        estimative_languageconfidence_in_analytic_judgment = self.estimative_languageconfidence_in_analytic_judgment

        estimative_languagelikelihood_probability = self.estimative_languagelikelihood_probability

        phishingpsychological_acceptability = self.phishingpsychological_acceptability

        phishingstate = self.phishingstate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "estimative-language:confidence-in-analytic-judgment": estimative_languageconfidence_in_analytic_judgment,
                "estimative-language:likelihood-probability": estimative_languagelikelihood_probability,
                "phishing:psychological-acceptability": phishingpsychological_acceptability,
                "phishing:state": phishingstate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        estimative_languageconfidence_in_analytic_judgment = d.pop(
            "estimative-language:confidence-in-analytic-judgment"
        )

        estimative_languagelikelihood_probability = d.pop("estimative-language:likelihood-probability")

        phishingpsychological_acceptability = d.pop("phishing:psychological-acceptability")

        phishingstate = d.pop("phishing:state")

        search_attributes_model_overrides_base_score_config = cls(
            estimative_languageconfidence_in_analytic_judgment=estimative_languageconfidence_in_analytic_judgment,
            estimative_languagelikelihood_probability=estimative_languagelikelihood_probability,
            phishingpsychological_acceptability=phishingpsychological_acceptability,
            phishingstate=phishingstate,
        )

        search_attributes_model_overrides_base_score_config.additional_properties = d
        return search_attributes_model_overrides_base_score_config

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
