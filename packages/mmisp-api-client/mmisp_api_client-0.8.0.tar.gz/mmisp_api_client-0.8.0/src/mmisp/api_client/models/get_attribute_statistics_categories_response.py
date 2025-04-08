from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAttributeStatisticsCategoriesResponse")


@_attrs_define
class GetAttributeStatisticsCategoriesResponse:
    """
    Attributes:
        payload_delivery (Union[Unset, str]):
        artifacts_dropped (Union[Unset, str]):
        payload_installation (Union[Unset, str]):
        external_analysis (Union[Unset, str]):
        persistence_mechanism (Union[Unset, str]):
        network_activity (Union[Unset, str]):
        attribution (Union[Unset, str]):
        social_network (Union[Unset, str]):
        person (Union[Unset, str]):
        other (Union[Unset, str]):
        internal_reference (Union[Unset, str]):
        antivirus_detection (Union[Unset, str]):
        support_tool (Union[Unset, str]):
        targeting_data (Union[Unset, str]):
        payload_type (Union[Unset, str]):
        financial_fraud (Union[Unset, str]):
    """

    payload_delivery: Union[Unset, str] = UNSET
    artifacts_dropped: Union[Unset, str] = UNSET
    payload_installation: Union[Unset, str] = UNSET
    external_analysis: Union[Unset, str] = UNSET
    persistence_mechanism: Union[Unset, str] = UNSET
    network_activity: Union[Unset, str] = UNSET
    attribution: Union[Unset, str] = UNSET
    social_network: Union[Unset, str] = UNSET
    person: Union[Unset, str] = UNSET
    other: Union[Unset, str] = UNSET
    internal_reference: Union[Unset, str] = UNSET
    antivirus_detection: Union[Unset, str] = UNSET
    support_tool: Union[Unset, str] = UNSET
    targeting_data: Union[Unset, str] = UNSET
    payload_type: Union[Unset, str] = UNSET
    financial_fraud: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload_delivery = self.payload_delivery

        artifacts_dropped = self.artifacts_dropped

        payload_installation = self.payload_installation

        external_analysis = self.external_analysis

        persistence_mechanism = self.persistence_mechanism

        network_activity = self.network_activity

        attribution = self.attribution

        social_network = self.social_network

        person = self.person

        other = self.other

        internal_reference = self.internal_reference

        antivirus_detection = self.antivirus_detection

        support_tool = self.support_tool

        targeting_data = self.targeting_data

        payload_type = self.payload_type

        financial_fraud = self.financial_fraud

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payload_delivery is not UNSET:
            field_dict["Payload delivery"] = payload_delivery
        if artifacts_dropped is not UNSET:
            field_dict["Artifacts dropped"] = artifacts_dropped
        if payload_installation is not UNSET:
            field_dict["Payload installation"] = payload_installation
        if external_analysis is not UNSET:
            field_dict["External analysis"] = external_analysis
        if persistence_mechanism is not UNSET:
            field_dict["Persistence mechanism"] = persistence_mechanism
        if network_activity is not UNSET:
            field_dict["Network activity"] = network_activity
        if attribution is not UNSET:
            field_dict["Attribution"] = attribution
        if social_network is not UNSET:
            field_dict["Social network"] = social_network
        if person is not UNSET:
            field_dict["Person"] = person
        if other is not UNSET:
            field_dict["Other"] = other
        if internal_reference is not UNSET:
            field_dict["Internal reference"] = internal_reference
        if antivirus_detection is not UNSET:
            field_dict["Antivirus detection"] = antivirus_detection
        if support_tool is not UNSET:
            field_dict["Support Tool"] = support_tool
        if targeting_data is not UNSET:
            field_dict["Targeting data"] = targeting_data
        if payload_type is not UNSET:
            field_dict["Payload type"] = payload_type
        if financial_fraud is not UNSET:
            field_dict["Financial fraud"] = financial_fraud

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payload_delivery = d.pop("Payload delivery", UNSET)

        artifacts_dropped = d.pop("Artifacts dropped", UNSET)

        payload_installation = d.pop("Payload installation", UNSET)

        external_analysis = d.pop("External analysis", UNSET)

        persistence_mechanism = d.pop("Persistence mechanism", UNSET)

        network_activity = d.pop("Network activity", UNSET)

        attribution = d.pop("Attribution", UNSET)

        social_network = d.pop("Social network", UNSET)

        person = d.pop("Person", UNSET)

        other = d.pop("Other", UNSET)

        internal_reference = d.pop("Internal reference", UNSET)

        antivirus_detection = d.pop("Antivirus detection", UNSET)

        support_tool = d.pop("Support Tool", UNSET)

        targeting_data = d.pop("Targeting data", UNSET)

        payload_type = d.pop("Payload type", UNSET)

        financial_fraud = d.pop("Financial fraud", UNSET)

        get_attribute_statistics_categories_response = cls(
            payload_delivery=payload_delivery,
            artifacts_dropped=artifacts_dropped,
            payload_installation=payload_installation,
            external_analysis=external_analysis,
            persistence_mechanism=persistence_mechanism,
            network_activity=network_activity,
            attribution=attribution,
            social_network=social_network,
            person=person,
            other=other,
            internal_reference=internal_reference,
            antivirus_detection=antivirus_detection,
            support_tool=support_tool,
            targeting_data=targeting_data,
            payload_type=payload_type,
            financial_fraud=financial_fraud,
        )

        get_attribute_statistics_categories_response.additional_properties = d
        return get_attribute_statistics_categories_response

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
