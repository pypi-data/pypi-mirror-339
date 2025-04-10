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

from ..models.contracts_for_difference_underlying_type_enum import ContractsForDifferenceUnderlyingTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentContractsForDifferenceData")


@_attrs_define
class FinancialInstrumentContractsForDifferenceData:
    """
    Attributes:
        underlying_type (Union[Unset, ContractsForDifferenceUnderlyingTypeEnum]):
        notional_currency_1 (Union[Unset, str]):
        notional_currency_2 (Union[Unset, str]):
    """

    underlying_type: Union[Unset, ContractsForDifferenceUnderlyingTypeEnum] = UNSET
    notional_currency_1: Union[Unset, str] = UNSET
    notional_currency_2: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        underlying_type: Union[Unset, str] = UNSET
        if not isinstance(self.underlying_type, Unset):
            underlying_type = self.underlying_type.value

        notional_currency_1 = self.notional_currency_1

        notional_currency_2 = self.notional_currency_2

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if underlying_type is not UNSET:
            field_dict["underlyingType"] = underlying_type
        if notional_currency_1 is not UNSET:
            field_dict["notionalCurrency1"] = notional_currency_1
        if notional_currency_2 is not UNSET:
            field_dict["notionalCurrency2"] = notional_currency_2

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _underlying_type = d.pop("underlyingType", UNSET)
        underlying_type: Union[Unset, ContractsForDifferenceUnderlyingTypeEnum]
        if isinstance(_underlying_type, Unset):
            underlying_type = UNSET
        else:
            underlying_type = ContractsForDifferenceUnderlyingTypeEnum(_underlying_type)

        notional_currency_1 = d.pop("notionalCurrency1", UNSET)

        notional_currency_2 = d.pop("notionalCurrency2", UNSET)

        financial_instrument_contracts_for_difference_data = cls(
            underlying_type=underlying_type,
            notional_currency_1=notional_currency_1,
            notional_currency_2=notional_currency_2,
        )

        financial_instrument_contracts_for_difference_data.additional_properties = d
        return financial_instrument_contracts_for_difference_data

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
