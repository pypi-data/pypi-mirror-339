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
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentCreditDerivativeData")


@_attrs_define
class FinancialInstrumentCreditDerivativeData:
    """
    Attributes:
        underlying_swap_isin (Union[Unset, str]):
        underlying_index_isin (Union[Unset, str]):
        underlying_index_name (Union[Unset, str]):
        series (Union[Unset, str]):
        version (Union[Unset, str]):
        roll_months (Union[Unset, list[str]]):
        next_roll_date (Union[Unset, datetime.date]):
        issuer_sovereign_public (Union[Unset, bool]):  Default: False.
        reference_obligation_isin (Union[Unset, str]):
        reference_entity_country (Union[Unset, str]):
        reference_entity_sub_division (Union[Unset, str]):
        reference_entity_lei (Union[Unset, str]):
        reference_entity_notional_currency (Union[Unset, str]):
    """

    underlying_swap_isin: Union[Unset, str] = UNSET
    underlying_index_isin: Union[Unset, str] = UNSET
    underlying_index_name: Union[Unset, str] = UNSET
    series: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    roll_months: Union[Unset, list[str]] = UNSET
    next_roll_date: Union[Unset, datetime.date] = UNSET
    issuer_sovereign_public: Union[Unset, bool] = False
    reference_obligation_isin: Union[Unset, str] = UNSET
    reference_entity_country: Union[Unset, str] = UNSET
    reference_entity_sub_division: Union[Unset, str] = UNSET
    reference_entity_lei: Union[Unset, str] = UNSET
    reference_entity_notional_currency: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        underlying_swap_isin = self.underlying_swap_isin

        underlying_index_isin = self.underlying_index_isin

        underlying_index_name = self.underlying_index_name

        series = self.series

        version = self.version

        roll_months: Union[Unset, list[str]] = UNSET
        if not isinstance(self.roll_months, Unset):
            roll_months = self.roll_months

        next_roll_date: Union[Unset, str] = UNSET
        if not isinstance(self.next_roll_date, Unset):
            next_roll_date = self.next_roll_date.isoformat()

        issuer_sovereign_public = self.issuer_sovereign_public

        reference_obligation_isin = self.reference_obligation_isin

        reference_entity_country = self.reference_entity_country

        reference_entity_sub_division = self.reference_entity_sub_division

        reference_entity_lei = self.reference_entity_lei

        reference_entity_notional_currency = self.reference_entity_notional_currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if underlying_swap_isin is not UNSET:
            field_dict["underlyingSwapIsin"] = underlying_swap_isin
        if underlying_index_isin is not UNSET:
            field_dict["underlyingIndexIsin"] = underlying_index_isin
        if underlying_index_name is not UNSET:
            field_dict["underlyingIndexName"] = underlying_index_name
        if series is not UNSET:
            field_dict["series"] = series
        if version is not UNSET:
            field_dict["version"] = version
        if roll_months is not UNSET:
            field_dict["rollMonths"] = roll_months
        if next_roll_date is not UNSET:
            field_dict["nextRollDate"] = next_roll_date
        if issuer_sovereign_public is not UNSET:
            field_dict["issuerSovereignPublic"] = issuer_sovereign_public
        if reference_obligation_isin is not UNSET:
            field_dict["referenceObligationIsin"] = reference_obligation_isin
        if reference_entity_country is not UNSET:
            field_dict["referenceEntityCountry"] = reference_entity_country
        if reference_entity_sub_division is not UNSET:
            field_dict["referenceEntitySubDivision"] = reference_entity_sub_division
        if reference_entity_lei is not UNSET:
            field_dict["referenceEntityLei"] = reference_entity_lei
        if reference_entity_notional_currency is not UNSET:
            field_dict["referenceEntityNotionalCurrency"] = reference_entity_notional_currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        underlying_swap_isin = d.pop("underlyingSwapIsin", UNSET)

        underlying_index_isin = d.pop("underlyingIndexIsin", UNSET)

        underlying_index_name = d.pop("underlyingIndexName", UNSET)

        series = d.pop("series", UNSET)

        version = d.pop("version", UNSET)

        roll_months = cast(list[str], d.pop("rollMonths", UNSET))

        _next_roll_date = d.pop("nextRollDate", UNSET)
        next_roll_date: Union[Unset, datetime.date]
        if isinstance(_next_roll_date, Unset):
            next_roll_date = UNSET
        else:
            next_roll_date = isoparse(_next_roll_date).date()

        issuer_sovereign_public = d.pop("issuerSovereignPublic", UNSET)

        reference_obligation_isin = d.pop("referenceObligationIsin", UNSET)

        reference_entity_country = d.pop("referenceEntityCountry", UNSET)

        reference_entity_sub_division = d.pop("referenceEntitySubDivision", UNSET)

        reference_entity_lei = d.pop("referenceEntityLei", UNSET)

        reference_entity_notional_currency = d.pop("referenceEntityNotionalCurrency", UNSET)

        financial_instrument_credit_derivative_data = cls(
            underlying_swap_isin=underlying_swap_isin,
            underlying_index_isin=underlying_index_isin,
            underlying_index_name=underlying_index_name,
            series=series,
            version=version,
            roll_months=roll_months,
            next_roll_date=next_roll_date,
            issuer_sovereign_public=issuer_sovereign_public,
            reference_obligation_isin=reference_obligation_isin,
            reference_entity_country=reference_entity_country,
            reference_entity_sub_division=reference_entity_sub_division,
            reference_entity_lei=reference_entity_lei,
            reference_entity_notional_currency=reference_entity_notional_currency,
        )

        financial_instrument_credit_derivative_data.additional_properties = d
        return financial_instrument_credit_derivative_data

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
