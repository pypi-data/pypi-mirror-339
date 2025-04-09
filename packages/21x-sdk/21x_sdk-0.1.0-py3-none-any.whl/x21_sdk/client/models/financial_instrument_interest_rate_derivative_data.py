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
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.financial_instrument_index_term_unit_enum import FinancialInstrumentIndexTermUnitEnum
from ..models.index_definition_enum import IndexDefinitionEnum
from ..models.interest_rate_derivative_underlying_type_enum import InterestRateDerivativeUnderlyingTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.underlying_interest_rate_derivative_bond_data import UnderlyingInterestRateDerivativeBondData
    from ..models.underlying_interest_rate_derivative_swap_data import UnderlyingInterestRateDerivativeSwapData


T = TypeVar("T", bound="FinancialInstrumentInterestRateDerivativeData")


@_attrs_define
class FinancialInstrumentInterestRateDerivativeData:
    """
    Attributes:
        reference_rate_index (Union[Unset, IndexDefinitionEnum]):
        reference_rate_name (Union[Unset, str]):
        interest_rate_term_unit (Union[Unset, FinancialInstrumentIndexTermUnitEnum]):
        interest_rate_term_value (Union[Unset, int]):
        notional_currency_2 (Union[Unset, str]):
        fixed_rate_leg_1 (Union[Unset, str]):
        fixed_rate_leg_2 (Union[Unset, str]):
        floating_rate_leg_2_index (Union[Unset, IndexDefinitionEnum]):
        floating_rate_leg_2_name (Union[Unset, str]):
        interest_rate_leg_2_term_unit (Union[Unset, FinancialInstrumentIndexTermUnitEnum]):
        interest_rate_leg_2_term_value (Union[Unset, int]):
        underlying_interest_rate_derivative_type (Union[Unset, InterestRateDerivativeUnderlyingTypeEnum]):
        underlying_interest_rate_derivative_isin (Union[Unset, str]):
        underlying_interest_rate_derivative_index_name (Union[Unset, str]):
        underlying_interest_rate_derivative_reference_rate_index (Union[Unset, IndexDefinitionEnum]):
        underlying_interest_rate_derivative_reference_rate_name (Union[Unset, str]):
        underlying_interest_rate_derivative_term_unit (Union[Unset, FinancialInstrumentIndexTermUnitEnum]):
        underlying_interest_rate_derivative_term_value (Union[Unset, int]):
        underlying_interest_rate_derivative_bond (Union[Unset, UnderlyingInterestRateDerivativeBondData]):
        underlying_interest_rate_derivative_swap (Union[Unset, UnderlyingInterestRateDerivativeSwapData]):
    """

    reference_rate_index: Union[Unset, IndexDefinitionEnum] = UNSET
    reference_rate_name: Union[Unset, str] = UNSET
    interest_rate_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum] = UNSET
    interest_rate_term_value: Union[Unset, int] = UNSET
    notional_currency_2: Union[Unset, str] = UNSET
    fixed_rate_leg_1: Union[Unset, str] = UNSET
    fixed_rate_leg_2: Union[Unset, str] = UNSET
    floating_rate_leg_2_index: Union[Unset, IndexDefinitionEnum] = UNSET
    floating_rate_leg_2_name: Union[Unset, str] = UNSET
    interest_rate_leg_2_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum] = UNSET
    interest_rate_leg_2_term_value: Union[Unset, int] = UNSET
    underlying_interest_rate_derivative_type: Union[Unset, InterestRateDerivativeUnderlyingTypeEnum] = UNSET
    underlying_interest_rate_derivative_isin: Union[Unset, str] = UNSET
    underlying_interest_rate_derivative_index_name: Union[Unset, str] = UNSET
    underlying_interest_rate_derivative_reference_rate_index: Union[Unset, IndexDefinitionEnum] = UNSET
    underlying_interest_rate_derivative_reference_rate_name: Union[Unset, str] = UNSET
    underlying_interest_rate_derivative_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum] = UNSET
    underlying_interest_rate_derivative_term_value: Union[Unset, int] = UNSET
    underlying_interest_rate_derivative_bond: Union[Unset, "UnderlyingInterestRateDerivativeBondData"] = UNSET
    underlying_interest_rate_derivative_swap: Union[Unset, "UnderlyingInterestRateDerivativeSwapData"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reference_rate_index: Union[Unset, str] = UNSET
        if not isinstance(self.reference_rate_index, Unset):
            reference_rate_index = self.reference_rate_index.value

        reference_rate_name = self.reference_rate_name

        interest_rate_term_unit: Union[Unset, str] = UNSET
        if not isinstance(self.interest_rate_term_unit, Unset):
            interest_rate_term_unit = self.interest_rate_term_unit.value

        interest_rate_term_value = self.interest_rate_term_value

        notional_currency_2 = self.notional_currency_2

        fixed_rate_leg_1 = self.fixed_rate_leg_1

        fixed_rate_leg_2 = self.fixed_rate_leg_2

        floating_rate_leg_2_index: Union[Unset, str] = UNSET
        if not isinstance(self.floating_rate_leg_2_index, Unset):
            floating_rate_leg_2_index = self.floating_rate_leg_2_index.value

        floating_rate_leg_2_name = self.floating_rate_leg_2_name

        interest_rate_leg_2_term_unit: Union[Unset, str] = UNSET
        if not isinstance(self.interest_rate_leg_2_term_unit, Unset):
            interest_rate_leg_2_term_unit = self.interest_rate_leg_2_term_unit.value

        interest_rate_leg_2_term_value = self.interest_rate_leg_2_term_value

        underlying_interest_rate_derivative_type: Union[Unset, str] = UNSET
        if not isinstance(self.underlying_interest_rate_derivative_type, Unset):
            underlying_interest_rate_derivative_type = self.underlying_interest_rate_derivative_type.value

        underlying_interest_rate_derivative_isin = self.underlying_interest_rate_derivative_isin

        underlying_interest_rate_derivative_index_name = self.underlying_interest_rate_derivative_index_name

        underlying_interest_rate_derivative_reference_rate_index: Union[Unset, str] = UNSET
        if not isinstance(self.underlying_interest_rate_derivative_reference_rate_index, Unset):
            underlying_interest_rate_derivative_reference_rate_index = (
                self.underlying_interest_rate_derivative_reference_rate_index.value
            )

        underlying_interest_rate_derivative_reference_rate_name = (
            self.underlying_interest_rate_derivative_reference_rate_name
        )

        underlying_interest_rate_derivative_term_unit: Union[Unset, str] = UNSET
        if not isinstance(self.underlying_interest_rate_derivative_term_unit, Unset):
            underlying_interest_rate_derivative_term_unit = self.underlying_interest_rate_derivative_term_unit.value

        underlying_interest_rate_derivative_term_value = self.underlying_interest_rate_derivative_term_value

        underlying_interest_rate_derivative_bond: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.underlying_interest_rate_derivative_bond, Unset):
            underlying_interest_rate_derivative_bond = self.underlying_interest_rate_derivative_bond.to_dict()

        underlying_interest_rate_derivative_swap: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.underlying_interest_rate_derivative_swap, Unset):
            underlying_interest_rate_derivative_swap = self.underlying_interest_rate_derivative_swap.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if reference_rate_index is not UNSET:
            field_dict["referenceRateIndex"] = reference_rate_index
        if reference_rate_name is not UNSET:
            field_dict["referenceRateName"] = reference_rate_name
        if interest_rate_term_unit is not UNSET:
            field_dict["interestRateTermUnit"] = interest_rate_term_unit
        if interest_rate_term_value is not UNSET:
            field_dict["interestRateTermValue"] = interest_rate_term_value
        if notional_currency_2 is not UNSET:
            field_dict["notionalCurrency2"] = notional_currency_2
        if fixed_rate_leg_1 is not UNSET:
            field_dict["fixedRateLeg1"] = fixed_rate_leg_1
        if fixed_rate_leg_2 is not UNSET:
            field_dict["fixedRateLeg2"] = fixed_rate_leg_2
        if floating_rate_leg_2_index is not UNSET:
            field_dict["floatingRateLeg2Index"] = floating_rate_leg_2_index
        if floating_rate_leg_2_name is not UNSET:
            field_dict["floatingRateLeg2Name"] = floating_rate_leg_2_name
        if interest_rate_leg_2_term_unit is not UNSET:
            field_dict["interestRateLeg2TermUnit"] = interest_rate_leg_2_term_unit
        if interest_rate_leg_2_term_value is not UNSET:
            field_dict["interestRateLeg2TermValue"] = interest_rate_leg_2_term_value
        if underlying_interest_rate_derivative_type is not UNSET:
            field_dict["underlyingInterestRateDerivativeType"] = underlying_interest_rate_derivative_type
        if underlying_interest_rate_derivative_isin is not UNSET:
            field_dict["underlyingInterestRateDerivativeIsin"] = underlying_interest_rate_derivative_isin
        if underlying_interest_rate_derivative_index_name is not UNSET:
            field_dict["underlyingInterestRateDerivativeIndexName"] = underlying_interest_rate_derivative_index_name
        if underlying_interest_rate_derivative_reference_rate_index is not UNSET:
            field_dict["underlyingInterestRateDerivativeReferenceRateIndex"] = (
                underlying_interest_rate_derivative_reference_rate_index
            )
        if underlying_interest_rate_derivative_reference_rate_name is not UNSET:
            field_dict["underlyingInterestRateDerivativeReferenceRateName"] = (
                underlying_interest_rate_derivative_reference_rate_name
            )
        if underlying_interest_rate_derivative_term_unit is not UNSET:
            field_dict["underlyingInterestRateDerivativeTermUnit"] = underlying_interest_rate_derivative_term_unit
        if underlying_interest_rate_derivative_term_value is not UNSET:
            field_dict["underlyingInterestRateDerivativeTermValue"] = underlying_interest_rate_derivative_term_value
        if underlying_interest_rate_derivative_bond is not UNSET:
            field_dict["underlyingInterestRateDerivativeBond"] = underlying_interest_rate_derivative_bond
        if underlying_interest_rate_derivative_swap is not UNSET:
            field_dict["underlyingInterestRateDerivativeSwap"] = underlying_interest_rate_derivative_swap

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.underlying_interest_rate_derivative_bond_data import UnderlyingInterestRateDerivativeBondData
        from ..models.underlying_interest_rate_derivative_swap_data import UnderlyingInterestRateDerivativeSwapData

        d = dict(src_dict)
        _reference_rate_index = d.pop("referenceRateIndex", UNSET)
        reference_rate_index: Union[Unset, IndexDefinitionEnum]
        if isinstance(_reference_rate_index, Unset):
            reference_rate_index = UNSET
        else:
            reference_rate_index = IndexDefinitionEnum(_reference_rate_index)

        reference_rate_name = d.pop("referenceRateName", UNSET)

        _interest_rate_term_unit = d.pop("interestRateTermUnit", UNSET)
        interest_rate_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum]
        if isinstance(_interest_rate_term_unit, Unset):
            interest_rate_term_unit = UNSET
        else:
            interest_rate_term_unit = FinancialInstrumentIndexTermUnitEnum(_interest_rate_term_unit)

        interest_rate_term_value = d.pop("interestRateTermValue", UNSET)

        notional_currency_2 = d.pop("notionalCurrency2", UNSET)

        fixed_rate_leg_1 = d.pop("fixedRateLeg1", UNSET)

        fixed_rate_leg_2 = d.pop("fixedRateLeg2", UNSET)

        _floating_rate_leg_2_index = d.pop("floatingRateLeg2Index", UNSET)
        floating_rate_leg_2_index: Union[Unset, IndexDefinitionEnum]
        if isinstance(_floating_rate_leg_2_index, Unset):
            floating_rate_leg_2_index = UNSET
        else:
            floating_rate_leg_2_index = IndexDefinitionEnum(_floating_rate_leg_2_index)

        floating_rate_leg_2_name = d.pop("floatingRateLeg2Name", UNSET)

        _interest_rate_leg_2_term_unit = d.pop("interestRateLeg2TermUnit", UNSET)
        interest_rate_leg_2_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum]
        if isinstance(_interest_rate_leg_2_term_unit, Unset):
            interest_rate_leg_2_term_unit = UNSET
        else:
            interest_rate_leg_2_term_unit = FinancialInstrumentIndexTermUnitEnum(_interest_rate_leg_2_term_unit)

        interest_rate_leg_2_term_value = d.pop("interestRateLeg2TermValue", UNSET)

        _underlying_interest_rate_derivative_type = d.pop("underlyingInterestRateDerivativeType", UNSET)
        underlying_interest_rate_derivative_type: Union[Unset, InterestRateDerivativeUnderlyingTypeEnum]
        if isinstance(_underlying_interest_rate_derivative_type, Unset):
            underlying_interest_rate_derivative_type = UNSET
        else:
            underlying_interest_rate_derivative_type = InterestRateDerivativeUnderlyingTypeEnum(
                _underlying_interest_rate_derivative_type
            )

        underlying_interest_rate_derivative_isin = d.pop("underlyingInterestRateDerivativeIsin", UNSET)

        underlying_interest_rate_derivative_index_name = d.pop("underlyingInterestRateDerivativeIndexName", UNSET)

        _underlying_interest_rate_derivative_reference_rate_index = d.pop(
            "underlyingInterestRateDerivativeReferenceRateIndex", UNSET
        )
        underlying_interest_rate_derivative_reference_rate_index: Union[Unset, IndexDefinitionEnum]
        if isinstance(_underlying_interest_rate_derivative_reference_rate_index, Unset):
            underlying_interest_rate_derivative_reference_rate_index = UNSET
        else:
            underlying_interest_rate_derivative_reference_rate_index = IndexDefinitionEnum(
                _underlying_interest_rate_derivative_reference_rate_index
            )

        underlying_interest_rate_derivative_reference_rate_name = d.pop(
            "underlyingInterestRateDerivativeReferenceRateName", UNSET
        )

        _underlying_interest_rate_derivative_term_unit = d.pop("underlyingInterestRateDerivativeTermUnit", UNSET)
        underlying_interest_rate_derivative_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum]
        if isinstance(_underlying_interest_rate_derivative_term_unit, Unset):
            underlying_interest_rate_derivative_term_unit = UNSET
        else:
            underlying_interest_rate_derivative_term_unit = FinancialInstrumentIndexTermUnitEnum(
                _underlying_interest_rate_derivative_term_unit
            )

        underlying_interest_rate_derivative_term_value = d.pop("underlyingInterestRateDerivativeTermValue", UNSET)

        _underlying_interest_rate_derivative_bond = d.pop("underlyingInterestRateDerivativeBond", UNSET)
        underlying_interest_rate_derivative_bond: Union[Unset, UnderlyingInterestRateDerivativeBondData]
        if isinstance(_underlying_interest_rate_derivative_bond, Unset):
            underlying_interest_rate_derivative_bond = UNSET
        else:
            underlying_interest_rate_derivative_bond = UnderlyingInterestRateDerivativeBondData.from_dict(
                _underlying_interest_rate_derivative_bond
            )

        _underlying_interest_rate_derivative_swap = d.pop("underlyingInterestRateDerivativeSwap", UNSET)
        underlying_interest_rate_derivative_swap: Union[Unset, UnderlyingInterestRateDerivativeSwapData]
        if isinstance(_underlying_interest_rate_derivative_swap, Unset):
            underlying_interest_rate_derivative_swap = UNSET
        else:
            underlying_interest_rate_derivative_swap = UnderlyingInterestRateDerivativeSwapData.from_dict(
                _underlying_interest_rate_derivative_swap
            )

        financial_instrument_interest_rate_derivative_data = cls(
            reference_rate_index=reference_rate_index,
            reference_rate_name=reference_rate_name,
            interest_rate_term_unit=interest_rate_term_unit,
            interest_rate_term_value=interest_rate_term_value,
            notional_currency_2=notional_currency_2,
            fixed_rate_leg_1=fixed_rate_leg_1,
            fixed_rate_leg_2=fixed_rate_leg_2,
            floating_rate_leg_2_index=floating_rate_leg_2_index,
            floating_rate_leg_2_name=floating_rate_leg_2_name,
            interest_rate_leg_2_term_unit=interest_rate_leg_2_term_unit,
            interest_rate_leg_2_term_value=interest_rate_leg_2_term_value,
            underlying_interest_rate_derivative_type=underlying_interest_rate_derivative_type,
            underlying_interest_rate_derivative_isin=underlying_interest_rate_derivative_isin,
            underlying_interest_rate_derivative_index_name=underlying_interest_rate_derivative_index_name,
            underlying_interest_rate_derivative_reference_rate_index=underlying_interest_rate_derivative_reference_rate_index,
            underlying_interest_rate_derivative_reference_rate_name=underlying_interest_rate_derivative_reference_rate_name,
            underlying_interest_rate_derivative_term_unit=underlying_interest_rate_derivative_term_unit,
            underlying_interest_rate_derivative_term_value=underlying_interest_rate_derivative_term_value,
            underlying_interest_rate_derivative_bond=underlying_interest_rate_derivative_bond,
            underlying_interest_rate_derivative_swap=underlying_interest_rate_derivative_swap,
        )

        financial_instrument_interest_rate_derivative_data.additional_properties = d
        return financial_instrument_interest_rate_derivative_data

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
