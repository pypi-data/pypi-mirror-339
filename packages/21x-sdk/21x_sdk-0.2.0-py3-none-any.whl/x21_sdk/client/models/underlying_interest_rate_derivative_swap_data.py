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
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnderlyingInterestRateDerivativeSwapData")


@_attrs_define
class UnderlyingInterestRateDerivativeSwapData:
    """
    Attributes:
        notional_currency (Union[Unset, str]):
        maturity_date (Union[Unset, datetime.date]):
    """

    notional_currency: Union[Unset, str] = UNSET
    maturity_date: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        notional_currency = self.notional_currency

        maturity_date: Union[Unset, str] = UNSET
        if not isinstance(self.maturity_date, Unset):
            maturity_date = self.maturity_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if notional_currency is not UNSET:
            field_dict["notionalCurrency"] = notional_currency
        if maturity_date is not UNSET:
            field_dict["maturityDate"] = maturity_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        notional_currency = d.pop("notionalCurrency", UNSET)

        _maturity_date = d.pop("maturityDate", UNSET)
        maturity_date: Union[Unset, datetime.date]
        if isinstance(_maturity_date, Unset):
            maturity_date = UNSET
        else:
            maturity_date = isoparse(_maturity_date).date()

        underlying_interest_rate_derivative_swap_data = cls(
            notional_currency=notional_currency,
            maturity_date=maturity_date,
        )

        underlying_interest_rate_derivative_swap_data.additional_properties = d
        return underlying_interest_rate_derivative_swap_data

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
