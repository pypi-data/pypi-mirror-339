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

T = TypeVar("T", bound="UnderlyingInterestRateDerivativeBondData")


@_attrs_define
class UnderlyingInterestRateDerivativeBondData:
    """
    Attributes:
        issuer_lei (Union[Unset, str]):
        maturity_date (Union[Unset, datetime.date]):
        issuance_date (Union[Unset, datetime.date]):
    """

    issuer_lei: Union[Unset, str] = UNSET
    maturity_date: Union[Unset, datetime.date] = UNSET
    issuance_date: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        issuer_lei = self.issuer_lei

        maturity_date: Union[Unset, str] = UNSET
        if not isinstance(self.maturity_date, Unset):
            maturity_date = self.maturity_date.isoformat()

        issuance_date: Union[Unset, str] = UNSET
        if not isinstance(self.issuance_date, Unset):
            issuance_date = self.issuance_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if issuer_lei is not UNSET:
            field_dict["issuerLei"] = issuer_lei
        if maturity_date is not UNSET:
            field_dict["maturityDate"] = maturity_date
        if issuance_date is not UNSET:
            field_dict["issuanceDate"] = issuance_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        issuer_lei = d.pop("issuerLei", UNSET)

        _maturity_date = d.pop("maturityDate", UNSET)
        maturity_date: Union[Unset, datetime.date]
        if isinstance(_maturity_date, Unset):
            maturity_date = UNSET
        else:
            maturity_date = isoparse(_maturity_date).date()

        _issuance_date = d.pop("issuanceDate", UNSET)
        issuance_date: Union[Unset, datetime.date]
        if isinstance(_issuance_date, Unset):
            issuance_date = UNSET
        else:
            issuance_date = isoparse(_issuance_date).date()

        underlying_interest_rate_derivative_bond_data = cls(
            issuer_lei=issuer_lei,
            maturity_date=maturity_date,
            issuance_date=issuance_date,
        )

        underlying_interest_rate_derivative_bond_data.additional_properties = d
        return underlying_interest_rate_derivative_bond_data

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
