# Copyright 2025 21X AG
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.financial_instrument_classification_enum import FinancialInstrumentClassificationEnum
from ..models.financial_instrument_distribution_enum import FinancialInstrumentDistributionEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentAvailabilityData")


@_attrs_define
class FinancialInstrumentAvailabilityData:
    """
    Attributes:
        classification (Union[Unset, list[FinancialInstrumentClassificationEnum]]):
        distribution (Union[Unset, list[FinancialInstrumentDistributionEnum]]):
        jurisdictions (Union[Unset, list[str]]):
    """

    classification: Union[Unset, list[FinancialInstrumentClassificationEnum]] = UNSET
    distribution: Union[Unset, list[FinancialInstrumentDistributionEnum]] = UNSET
    jurisdictions: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        classification: Union[Unset, list[str]] = UNSET
        if not isinstance(self.classification, Unset):
            classification = []
            for classification_item_data in self.classification:
                classification_item = classification_item_data.value
                classification.append(classification_item)

        distribution: Union[Unset, list[str]] = UNSET
        if not isinstance(self.distribution, Unset):
            distribution = []
            for distribution_item_data in self.distribution:
                distribution_item = distribution_item_data.value
                distribution.append(distribution_item)

        jurisdictions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.jurisdictions, Unset):
            jurisdictions = self.jurisdictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if classification is not UNSET:
            field_dict["classification"] = classification
        if distribution is not UNSET:
            field_dict["distribution"] = distribution
        if jurisdictions is not UNSET:
            field_dict["jurisdictions"] = jurisdictions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        classification = []
        _classification = d.pop("classification", UNSET)
        for classification_item_data in _classification or []:
            classification_item = FinancialInstrumentClassificationEnum(classification_item_data)

            classification.append(classification_item)

        distribution = []
        _distribution = d.pop("distribution", UNSET)
        for distribution_item_data in _distribution or []:
            distribution_item = FinancialInstrumentDistributionEnum(distribution_item_data)

            distribution.append(distribution_item)

        jurisdictions = cast(list[str], d.pop("jurisdictions", UNSET))

        financial_instrument_availability_data = cls(
            classification=classification,
            distribution=distribution,
            jurisdictions=jurisdictions,
        )

        financial_instrument_availability_data.additional_properties = d
        return financial_instrument_availability_data

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
