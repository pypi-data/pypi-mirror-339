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
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentFilterCriteria")


@_attrs_define
class FinancialInstrumentFilterCriteria:
    """
    Attributes:
        primary_market (Union[Unset, bool]):
        secondary_market (Union[Unset, bool]):
    """

    primary_market: Union[Unset, bool] = UNSET
    secondary_market: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        primary_market = self.primary_market

        secondary_market = self.secondary_market

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if primary_market is not UNSET:
            field_dict["primaryMarket"] = primary_market
        if secondary_market is not UNSET:
            field_dict["secondaryMarket"] = secondary_market

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        primary_market = d.pop("primaryMarket", UNSET)

        secondary_market = d.pop("secondaryMarket", UNSET)

        financial_instrument_filter_criteria = cls(
            primary_market=primary_market,
            secondary_market=secondary_market,
        )

        financial_instrument_filter_criteria.additional_properties = d
        return financial_instrument_filter_criteria

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
