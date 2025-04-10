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

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.financial_instrument_bond_type_enum import FinancialInstrumentBondTypeEnum
from ..models.financial_instrument_seniority_enum import FinancialInstrumentSeniorityEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.financial_instrument_index_benchmark_data import FinancialInstrumentIndexBenchmarkData


T = TypeVar("T", bound="FinancialInstrumentDebtInstrumentData")


@_attrs_define
class FinancialInstrumentDebtInstrumentData:
    """
    Attributes:
        total_issued_nominal_amount (Union[Unset, str]):
        maturity_date (Union[Unset, datetime.date]):
        currency (Union[Unset, str]):
        minimum_traded_value (Union[Unset, str]):
        fixed_rate (Union[Unset, str]):
        bond_seniority (Union[Unset, FinancialInstrumentSeniorityEnum]):
        bond_type (Union[Unset, FinancialInstrumentBondTypeEnum]):
        bond_issuance_date (Union[Unset, datetime.date]):
        index_benchmark (Union[Unset, FinancialInstrumentIndexBenchmarkData]):
    """

    total_issued_nominal_amount: Union[Unset, str] = UNSET
    maturity_date: Union[Unset, datetime.date] = UNSET
    currency: Union[Unset, str] = UNSET
    minimum_traded_value: Union[Unset, str] = UNSET
    fixed_rate: Union[Unset, str] = UNSET
    bond_seniority: Union[Unset, FinancialInstrumentSeniorityEnum] = UNSET
    bond_type: Union[Unset, FinancialInstrumentBondTypeEnum] = UNSET
    bond_issuance_date: Union[Unset, datetime.date] = UNSET
    index_benchmark: Union[Unset, "FinancialInstrumentIndexBenchmarkData"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_issued_nominal_amount = self.total_issued_nominal_amount

        maturity_date: Union[Unset, str] = UNSET
        if not isinstance(self.maturity_date, Unset):
            maturity_date = self.maturity_date.isoformat()

        currency = self.currency

        minimum_traded_value = self.minimum_traded_value

        fixed_rate = self.fixed_rate

        bond_seniority: Union[Unset, str] = UNSET
        if not isinstance(self.bond_seniority, Unset):
            bond_seniority = self.bond_seniority.value

        bond_type: Union[Unset, str] = UNSET
        if not isinstance(self.bond_type, Unset):
            bond_type = self.bond_type.value

        bond_issuance_date: Union[Unset, str] = UNSET
        if not isinstance(self.bond_issuance_date, Unset):
            bond_issuance_date = self.bond_issuance_date.isoformat()

        index_benchmark: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.index_benchmark, Unset):
            index_benchmark = self.index_benchmark.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_issued_nominal_amount is not UNSET:
            field_dict["totalIssuedNominalAmount"] = total_issued_nominal_amount
        if maturity_date is not UNSET:
            field_dict["maturityDate"] = maturity_date
        if currency is not UNSET:
            field_dict["currency"] = currency
        if minimum_traded_value is not UNSET:
            field_dict["minimumTradedValue"] = minimum_traded_value
        if fixed_rate is not UNSET:
            field_dict["fixedRate"] = fixed_rate
        if bond_seniority is not UNSET:
            field_dict["bondSeniority"] = bond_seniority
        if bond_type is not UNSET:
            field_dict["bondType"] = bond_type
        if bond_issuance_date is not UNSET:
            field_dict["bondIssuanceDate"] = bond_issuance_date
        if index_benchmark is not UNSET:
            field_dict["indexBenchmark"] = index_benchmark

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.financial_instrument_index_benchmark_data import FinancialInstrumentIndexBenchmarkData

        d = dict(src_dict)
        total_issued_nominal_amount = d.pop("totalIssuedNominalAmount", UNSET)

        _maturity_date = d.pop("maturityDate", UNSET)
        maturity_date: Union[Unset, datetime.date]
        if isinstance(_maturity_date, Unset):
            maturity_date = UNSET
        else:
            maturity_date = isoparse(_maturity_date).date()

        currency = d.pop("currency", UNSET)

        minimum_traded_value = d.pop("minimumTradedValue", UNSET)

        fixed_rate = d.pop("fixedRate", UNSET)

        _bond_seniority = d.pop("bondSeniority", UNSET)
        bond_seniority: Union[Unset, FinancialInstrumentSeniorityEnum]
        if isinstance(_bond_seniority, Unset):
            bond_seniority = UNSET
        else:
            bond_seniority = FinancialInstrumentSeniorityEnum(_bond_seniority)

        _bond_type = d.pop("bondType", UNSET)
        bond_type: Union[Unset, FinancialInstrumentBondTypeEnum]
        if isinstance(_bond_type, Unset):
            bond_type = UNSET
        else:
            bond_type = FinancialInstrumentBondTypeEnum(_bond_type)

        _bond_issuance_date = d.pop("bondIssuanceDate", UNSET)
        bond_issuance_date: Union[Unset, datetime.date]
        if isinstance(_bond_issuance_date, Unset):
            bond_issuance_date = UNSET
        else:
            bond_issuance_date = isoparse(_bond_issuance_date).date()

        _index_benchmark = d.pop("indexBenchmark", UNSET)
        index_benchmark: Union[Unset, FinancialInstrumentIndexBenchmarkData]
        if isinstance(_index_benchmark, Unset):
            index_benchmark = UNSET
        else:
            index_benchmark = FinancialInstrumentIndexBenchmarkData.from_dict(_index_benchmark)

        financial_instrument_debt_instrument_data = cls(
            total_issued_nominal_amount=total_issued_nominal_amount,
            maturity_date=maturity_date,
            currency=currency,
            minimum_traded_value=minimum_traded_value,
            fixed_rate=fixed_rate,
            bond_seniority=bond_seniority,
            bond_type=bond_type,
            bond_issuance_date=bond_issuance_date,
            index_benchmark=index_benchmark,
        )

        financial_instrument_debt_instrument_data.additional_properties = d
        return financial_instrument_debt_instrument_data

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
