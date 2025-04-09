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

T = TypeVar("T", bound="FinancialInstrumentPerformanceData")


@_attrs_define
class FinancialInstrumentPerformanceData:
    """
    Attributes:
        nav (Union[Unset, str]):
        nav_currency (Union[Unset, str]):
        nav_last_update (Union[Unset, datetime.date]):
        nav_source (Union[Unset, str]):
        total_expense_ratio (Union[Unset, str]):
        assets_under_management (Union[Unset, str]):
        assets_under_management_currency (Union[Unset, str]):
        assets_under_management_last_update (Union[Unset, datetime.date]):
    """

    nav: Union[Unset, str] = UNSET
    nav_currency: Union[Unset, str] = UNSET
    nav_last_update: Union[Unset, datetime.date] = UNSET
    nav_source: Union[Unset, str] = UNSET
    total_expense_ratio: Union[Unset, str] = UNSET
    assets_under_management: Union[Unset, str] = UNSET
    assets_under_management_currency: Union[Unset, str] = UNSET
    assets_under_management_last_update: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nav = self.nav

        nav_currency = self.nav_currency

        nav_last_update: Union[Unset, str] = UNSET
        if not isinstance(self.nav_last_update, Unset):
            nav_last_update = self.nav_last_update.isoformat()

        nav_source = self.nav_source

        total_expense_ratio = self.total_expense_ratio

        assets_under_management = self.assets_under_management

        assets_under_management_currency = self.assets_under_management_currency

        assets_under_management_last_update: Union[Unset, str] = UNSET
        if not isinstance(self.assets_under_management_last_update, Unset):
            assets_under_management_last_update = self.assets_under_management_last_update.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if nav is not UNSET:
            field_dict["nav"] = nav
        if nav_currency is not UNSET:
            field_dict["navCurrency"] = nav_currency
        if nav_last_update is not UNSET:
            field_dict["navLastUpdate"] = nav_last_update
        if nav_source is not UNSET:
            field_dict["navSource"] = nav_source
        if total_expense_ratio is not UNSET:
            field_dict["totalExpenseRatio"] = total_expense_ratio
        if assets_under_management is not UNSET:
            field_dict["assetsUnderManagement"] = assets_under_management
        if assets_under_management_currency is not UNSET:
            field_dict["assetsUnderManagementCurrency"] = assets_under_management_currency
        if assets_under_management_last_update is not UNSET:
            field_dict["assetsUnderManagementLastUpdate"] = assets_under_management_last_update

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        nav = d.pop("nav", UNSET)

        nav_currency = d.pop("navCurrency", UNSET)

        _nav_last_update = d.pop("navLastUpdate", UNSET)
        nav_last_update: Union[Unset, datetime.date]
        if isinstance(_nav_last_update, Unset):
            nav_last_update = UNSET
        else:
            nav_last_update = isoparse(_nav_last_update).date()

        nav_source = d.pop("navSource", UNSET)

        total_expense_ratio = d.pop("totalExpenseRatio", UNSET)

        assets_under_management = d.pop("assetsUnderManagement", UNSET)

        assets_under_management_currency = d.pop("assetsUnderManagementCurrency", UNSET)

        _assets_under_management_last_update = d.pop("assetsUnderManagementLastUpdate", UNSET)
        assets_under_management_last_update: Union[Unset, datetime.date]
        if isinstance(_assets_under_management_last_update, Unset):
            assets_under_management_last_update = UNSET
        else:
            assets_under_management_last_update = isoparse(_assets_under_management_last_update).date()

        financial_instrument_performance_data = cls(
            nav=nav,
            nav_currency=nav_currency,
            nav_last_update=nav_last_update,
            nav_source=nav_source,
            total_expense_ratio=total_expense_ratio,
            assets_under_management=assets_under_management,
            assets_under_management_currency=assets_under_management_currency,
            assets_under_management_last_update=assets_under_management_last_update,
        )

        financial_instrument_performance_data.additional_properties = d
        return financial_instrument_performance_data

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
