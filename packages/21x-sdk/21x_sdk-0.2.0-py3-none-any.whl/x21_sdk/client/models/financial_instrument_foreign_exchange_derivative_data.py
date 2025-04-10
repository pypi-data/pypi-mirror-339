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

from ..models.foreign_exchange_derivative_contract_sub_type_enum import ForeignExchangeDerivativeContractSubTypeEnum
from ..models.foreign_exchange_derivative_type_enum import ForeignExchangeDerivativeTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentForeignExchangeDerivativeData")


@_attrs_define
class FinancialInstrumentForeignExchangeDerivativeData:
    """
    Attributes:
        notional_currency_2 (Union[Unset, str]):
        foreign_exchange_type (Union[Unset, ForeignExchangeDerivativeTypeEnum]):
        foreign_exchange_contract_sub_type (Union[Unset, ForeignExchangeDerivativeContractSubTypeEnum]):
    """

    notional_currency_2: Union[Unset, str] = UNSET
    foreign_exchange_type: Union[Unset, ForeignExchangeDerivativeTypeEnum] = UNSET
    foreign_exchange_contract_sub_type: Union[Unset, ForeignExchangeDerivativeContractSubTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        notional_currency_2 = self.notional_currency_2

        foreign_exchange_type: Union[Unset, str] = UNSET
        if not isinstance(self.foreign_exchange_type, Unset):
            foreign_exchange_type = self.foreign_exchange_type.value

        foreign_exchange_contract_sub_type: Union[Unset, str] = UNSET
        if not isinstance(self.foreign_exchange_contract_sub_type, Unset):
            foreign_exchange_contract_sub_type = self.foreign_exchange_contract_sub_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if notional_currency_2 is not UNSET:
            field_dict["notionalCurrency2"] = notional_currency_2
        if foreign_exchange_type is not UNSET:
            field_dict["foreignExchangeType"] = foreign_exchange_type
        if foreign_exchange_contract_sub_type is not UNSET:
            field_dict["foreignExchangeContractSubType"] = foreign_exchange_contract_sub_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        notional_currency_2 = d.pop("notionalCurrency2", UNSET)

        _foreign_exchange_type = d.pop("foreignExchangeType", UNSET)
        foreign_exchange_type: Union[Unset, ForeignExchangeDerivativeTypeEnum]
        if isinstance(_foreign_exchange_type, Unset):
            foreign_exchange_type = UNSET
        else:
            foreign_exchange_type = ForeignExchangeDerivativeTypeEnum(_foreign_exchange_type)

        _foreign_exchange_contract_sub_type = d.pop("foreignExchangeContractSubType", UNSET)
        foreign_exchange_contract_sub_type: Union[Unset, ForeignExchangeDerivativeContractSubTypeEnum]
        if isinstance(_foreign_exchange_contract_sub_type, Unset):
            foreign_exchange_contract_sub_type = UNSET
        else:
            foreign_exchange_contract_sub_type = ForeignExchangeDerivativeContractSubTypeEnum(
                _foreign_exchange_contract_sub_type
            )

        financial_instrument_foreign_exchange_derivative_data = cls(
            notional_currency_2=notional_currency_2,
            foreign_exchange_type=foreign_exchange_type,
            foreign_exchange_contract_sub_type=foreign_exchange_contract_sub_type,
        )

        financial_instrument_foreign_exchange_derivative_data.additional_properties = d
        return financial_instrument_foreign_exchange_derivative_data

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
