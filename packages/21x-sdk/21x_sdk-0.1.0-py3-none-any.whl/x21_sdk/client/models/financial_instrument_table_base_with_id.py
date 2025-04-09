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

from ..models.financial_instrument_status_enum import FinancialInstrumentStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentTableBaseWithId")


@_attrs_define
class FinancialInstrumentTableBaseWithId:
    """
    Attributes:
        symbol (Union[Unset, str]): The financial instrument's symbol
        full_name (Union[Unset, str]): The financial instrument's name
        status (Union[Unset, FinancialInstrumentStatusEnum]):
        isin (Union[Unset, str]): International Securities Identification Number (ISIN) of the financial instrument
        dti (Union[Unset, str]): Digital Token Identifier (DTI) of the financial instrument
        issuer_name (Union[Unset, str]): Name of the issuer of the financial instrument
        prospectus_link (Union[Unset, str]): Link to further information about the financial instrument
        effective_date (Union[Unset, datetime.datetime]): First day of active trading on 21X
        termination_date (Union[Unset, datetime.datetime]): Last day of trading on 21X
        smart_contract_address (Union[Unset, str]): The blockchain address of the financial instrument's smart contract
        internal_id (Union[Unset, str]):
    """

    symbol: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    status: Union[Unset, FinancialInstrumentStatusEnum] = UNSET
    isin: Union[Unset, str] = UNSET
    dti: Union[Unset, str] = UNSET
    issuer_name: Union[Unset, str] = UNSET
    prospectus_link: Union[Unset, str] = UNSET
    effective_date: Union[Unset, datetime.datetime] = UNSET
    termination_date: Union[Unset, datetime.datetime] = UNSET
    smart_contract_address: Union[Unset, str] = UNSET
    internal_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        full_name = self.full_name

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        isin = self.isin

        dti = self.dti

        issuer_name = self.issuer_name

        prospectus_link = self.prospectus_link

        effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        termination_date: Union[Unset, str] = UNSET
        if not isinstance(self.termination_date, Unset):
            termination_date = self.termination_date.isoformat()

        smart_contract_address = self.smart_contract_address

        internal_id = self.internal_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if status is not UNSET:
            field_dict["status"] = status
        if isin is not UNSET:
            field_dict["isin"] = isin
        if dti is not UNSET:
            field_dict["dti"] = dti
        if issuer_name is not UNSET:
            field_dict["issuerName"] = issuer_name
        if prospectus_link is not UNSET:
            field_dict["prospectusLink"] = prospectus_link
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date
        if termination_date is not UNSET:
            field_dict["terminationDate"] = termination_date
        if smart_contract_address is not UNSET:
            field_dict["smartContractAddress"] = smart_contract_address
        if internal_id is not UNSET:
            field_dict["internalId"] = internal_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol", UNSET)

        full_name = d.pop("fullName", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, FinancialInstrumentStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = FinancialInstrumentStatusEnum(_status)

        isin = d.pop("isin", UNSET)

        dti = d.pop("dti", UNSET)

        issuer_name = d.pop("issuerName", UNSET)

        prospectus_link = d.pop("prospectusLink", UNSET)

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: Union[Unset, datetime.datetime]
        if isinstance(_effective_date, Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date)

        _termination_date = d.pop("terminationDate", UNSET)
        termination_date: Union[Unset, datetime.datetime]
        if isinstance(_termination_date, Unset):
            termination_date = UNSET
        else:
            termination_date = isoparse(_termination_date)

        smart_contract_address = d.pop("smartContractAddress", UNSET)

        internal_id = d.pop("internalId", UNSET)

        financial_instrument_table_base_with_id = cls(
            symbol=symbol,
            full_name=full_name,
            status=status,
            isin=isin,
            dti=dti,
            issuer_name=issuer_name,
            prospectus_link=prospectus_link,
            effective_date=effective_date,
            termination_date=termination_date,
            smart_contract_address=smart_contract_address,
            internal_id=internal_id,
        )

        financial_instrument_table_base_with_id.additional_properties = d
        return financial_instrument_table_base_with_id

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
