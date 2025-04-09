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

from ..models.equity_derivative_parameter_type_enum import EquityDerivativeParameterTypeEnum
from ..models.equity_derivative_underlying_type_enum import EquityDerivativeUnderlyingTypeEnum
from ..models.financial_instrument_delivery_type_enum import FinancialInstrumentDeliveryTypeEnum
from ..models.financial_instrument_option_excercise_style_enum import FinancialInstrumentOptionExcerciseStyleEnum
from ..models.financial_instrument_option_type_enum import FinancialInstrumentOptionTypeEnum
from ..models.financial_instrument_strike_price_type_enum import FinancialInstrumentStrikePriceTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.financial_instrument_underlying_instrument_data import FinancialInstrumentUnderlyingInstrumentData


T = TypeVar("T", bound="FinancialInstrumentDerivativeData")


@_attrs_define
class FinancialInstrumentDerivativeData:
    """
    Attributes:
        expiry_date (Union[Unset, datetime.date]):
        price_multiplier (Union[Unset, str]):
        option_type (Union[Unset, FinancialInstrumentOptionTypeEnum]):
        strike_price_type (Union[Unset, FinancialInstrumentStrikePriceTypeEnum]):
        strike_price_value (Union[Unset, str]):
        strike_price_currency (Union[Unset, str]):
        option_exercise_style (Union[Unset, FinancialInstrumentOptionExcerciseStyleEnum]):
        delivery_type (Union[Unset, FinancialInstrumentDeliveryTypeEnum]):
        equity_derivative_underlying_type (Union[Unset, EquityDerivativeUnderlyingTypeEnum]):
        equity_derivative_parameter (Union[Unset, EquityDerivativeParameterTypeEnum]):
        underlying_instruments (Union[Unset, list['FinancialInstrumentUnderlyingInstrumentData']]):
    """

    expiry_date: Union[Unset, datetime.date] = UNSET
    price_multiplier: Union[Unset, str] = UNSET
    option_type: Union[Unset, FinancialInstrumentOptionTypeEnum] = UNSET
    strike_price_type: Union[Unset, FinancialInstrumentStrikePriceTypeEnum] = UNSET
    strike_price_value: Union[Unset, str] = UNSET
    strike_price_currency: Union[Unset, str] = UNSET
    option_exercise_style: Union[Unset, FinancialInstrumentOptionExcerciseStyleEnum] = UNSET
    delivery_type: Union[Unset, FinancialInstrumentDeliveryTypeEnum] = UNSET
    equity_derivative_underlying_type: Union[Unset, EquityDerivativeUnderlyingTypeEnum] = UNSET
    equity_derivative_parameter: Union[Unset, EquityDerivativeParameterTypeEnum] = UNSET
    underlying_instruments: Union[Unset, list["FinancialInstrumentUnderlyingInstrumentData"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiry_date: Union[Unset, str] = UNSET
        if not isinstance(self.expiry_date, Unset):
            expiry_date = self.expiry_date.isoformat()

        price_multiplier = self.price_multiplier

        option_type: Union[Unset, str] = UNSET
        if not isinstance(self.option_type, Unset):
            option_type = self.option_type.value

        strike_price_type: Union[Unset, str] = UNSET
        if not isinstance(self.strike_price_type, Unset):
            strike_price_type = self.strike_price_type.value

        strike_price_value = self.strike_price_value

        strike_price_currency = self.strike_price_currency

        option_exercise_style: Union[Unset, str] = UNSET
        if not isinstance(self.option_exercise_style, Unset):
            option_exercise_style = self.option_exercise_style.value

        delivery_type: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_type, Unset):
            delivery_type = self.delivery_type.value

        equity_derivative_underlying_type: Union[Unset, str] = UNSET
        if not isinstance(self.equity_derivative_underlying_type, Unset):
            equity_derivative_underlying_type = self.equity_derivative_underlying_type.value

        equity_derivative_parameter: Union[Unset, str] = UNSET
        if not isinstance(self.equity_derivative_parameter, Unset):
            equity_derivative_parameter = self.equity_derivative_parameter.value

        underlying_instruments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.underlying_instruments, Unset):
            underlying_instruments = []
            for underlying_instruments_item_data in self.underlying_instruments:
                underlying_instruments_item = underlying_instruments_item_data.to_dict()
                underlying_instruments.append(underlying_instruments_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expiry_date is not UNSET:
            field_dict["expiryDate"] = expiry_date
        if price_multiplier is not UNSET:
            field_dict["priceMultiplier"] = price_multiplier
        if option_type is not UNSET:
            field_dict["optionType"] = option_type
        if strike_price_type is not UNSET:
            field_dict["strikePriceType"] = strike_price_type
        if strike_price_value is not UNSET:
            field_dict["strikePriceValue"] = strike_price_value
        if strike_price_currency is not UNSET:
            field_dict["strikePriceCurrency"] = strike_price_currency
        if option_exercise_style is not UNSET:
            field_dict["optionExerciseStyle"] = option_exercise_style
        if delivery_type is not UNSET:
            field_dict["deliveryType"] = delivery_type
        if equity_derivative_underlying_type is not UNSET:
            field_dict["equityDerivativeUnderlyingType"] = equity_derivative_underlying_type
        if equity_derivative_parameter is not UNSET:
            field_dict["equityDerivativeParameter"] = equity_derivative_parameter
        if underlying_instruments is not UNSET:
            field_dict["underlyingInstruments"] = underlying_instruments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.financial_instrument_underlying_instrument_data import FinancialInstrumentUnderlyingInstrumentData

        d = dict(src_dict)
        _expiry_date = d.pop("expiryDate", UNSET)
        expiry_date: Union[Unset, datetime.date]
        if isinstance(_expiry_date, Unset):
            expiry_date = UNSET
        else:
            expiry_date = isoparse(_expiry_date).date()

        price_multiplier = d.pop("priceMultiplier", UNSET)

        _option_type = d.pop("optionType", UNSET)
        option_type: Union[Unset, FinancialInstrumentOptionTypeEnum]
        if isinstance(_option_type, Unset):
            option_type = UNSET
        else:
            option_type = FinancialInstrumentOptionTypeEnum(_option_type)

        _strike_price_type = d.pop("strikePriceType", UNSET)
        strike_price_type: Union[Unset, FinancialInstrumentStrikePriceTypeEnum]
        if isinstance(_strike_price_type, Unset):
            strike_price_type = UNSET
        else:
            strike_price_type = FinancialInstrumentStrikePriceTypeEnum(_strike_price_type)

        strike_price_value = d.pop("strikePriceValue", UNSET)

        strike_price_currency = d.pop("strikePriceCurrency", UNSET)

        _option_exercise_style = d.pop("optionExerciseStyle", UNSET)
        option_exercise_style: Union[Unset, FinancialInstrumentOptionExcerciseStyleEnum]
        if isinstance(_option_exercise_style, Unset):
            option_exercise_style = UNSET
        else:
            option_exercise_style = FinancialInstrumentOptionExcerciseStyleEnum(_option_exercise_style)

        _delivery_type = d.pop("deliveryType", UNSET)
        delivery_type: Union[Unset, FinancialInstrumentDeliveryTypeEnum]
        if isinstance(_delivery_type, Unset):
            delivery_type = UNSET
        else:
            delivery_type = FinancialInstrumentDeliveryTypeEnum(_delivery_type)

        _equity_derivative_underlying_type = d.pop("equityDerivativeUnderlyingType", UNSET)
        equity_derivative_underlying_type: Union[Unset, EquityDerivativeUnderlyingTypeEnum]
        if isinstance(_equity_derivative_underlying_type, Unset):
            equity_derivative_underlying_type = UNSET
        else:
            equity_derivative_underlying_type = EquityDerivativeUnderlyingTypeEnum(_equity_derivative_underlying_type)

        _equity_derivative_parameter = d.pop("equityDerivativeParameter", UNSET)
        equity_derivative_parameter: Union[Unset, EquityDerivativeParameterTypeEnum]
        if isinstance(_equity_derivative_parameter, Unset):
            equity_derivative_parameter = UNSET
        else:
            equity_derivative_parameter = EquityDerivativeParameterTypeEnum(_equity_derivative_parameter)

        underlying_instruments = []
        _underlying_instruments = d.pop("underlyingInstruments", UNSET)
        for underlying_instruments_item_data in _underlying_instruments or []:
            underlying_instruments_item = FinancialInstrumentUnderlyingInstrumentData.from_dict(
                underlying_instruments_item_data
            )

            underlying_instruments.append(underlying_instruments_item)

        financial_instrument_derivative_data = cls(
            expiry_date=expiry_date,
            price_multiplier=price_multiplier,
            option_type=option_type,
            strike_price_type=strike_price_type,
            strike_price_value=strike_price_value,
            strike_price_currency=strike_price_currency,
            option_exercise_style=option_exercise_style,
            delivery_type=delivery_type,
            equity_derivative_underlying_type=equity_derivative_underlying_type,
            equity_derivative_parameter=equity_derivative_parameter,
            underlying_instruments=underlying_instruments,
        )

        financial_instrument_derivative_data.additional_properties = d
        return financial_instrument_derivative_data

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
