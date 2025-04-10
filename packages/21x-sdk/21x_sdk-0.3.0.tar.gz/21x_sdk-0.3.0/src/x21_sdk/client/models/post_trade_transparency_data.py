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

T = TypeVar("T", bound="PostTradeTransparencyData")


@_attrs_define
class PostTradeTransparencyData:
    """
    Attributes:
        trading_date_time (datetime.datetime): Date and time of the finality of the transaction
        instrument_identification_code_type (str): The type of the instrument identification code, e.g. 'ISIN'
        instrument_identification_code (str): The identification code of the financial instrument
        price (str): The price at which the transaction was executed
        price_currency (str): Short code of the currency that the price is listed in
        price_notation (str): Usually 'MONE' for monetary value
        quantity (str): The number of units of the financial instrument that were traded
        venue_of_execution (str): MIC of the trading venue, e.g. '21XX'
        publication_date_time (datetime.datetime): Date and time that the transaction was published
        transaction_identification_code (str): Alpha-numeric string uniquely identifying each transaction
        notional_amount (str): The total monetary value of the transaction (price*quantity)
        notional_currency (Union[Unset, str]): Short code of the currency that the notional amount is listed in
    """

    trading_date_time: datetime.datetime
    instrument_identification_code_type: str
    instrument_identification_code: str
    price: str
    price_currency: str
    price_notation: str
    quantity: str
    venue_of_execution: str
    publication_date_time: datetime.datetime
    transaction_identification_code: str
    notional_amount: str
    notional_currency: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        trading_date_time = self.trading_date_time.isoformat()

        instrument_identification_code_type = self.instrument_identification_code_type

        instrument_identification_code = self.instrument_identification_code

        price = self.price

        price_currency = self.price_currency

        price_notation = self.price_notation

        quantity = self.quantity

        venue_of_execution = self.venue_of_execution

        publication_date_time = self.publication_date_time.isoformat()

        transaction_identification_code = self.transaction_identification_code

        notional_amount = self.notional_amount

        notional_currency = self.notional_currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tradingDateTime": trading_date_time,
                "instrumentIdentificationCodeType": instrument_identification_code_type,
                "instrumentIdentificationCode": instrument_identification_code,
                "price": price,
                "priceCurrency": price_currency,
                "priceNotation": price_notation,
                "quantity": quantity,
                "venueOfExecution": venue_of_execution,
                "publicationDateTime": publication_date_time,
                "transactionIdentificationCode": transaction_identification_code,
                "notionalAmount": notional_amount,
            }
        )
        if notional_currency is not UNSET:
            field_dict["notionalCurrency"] = notional_currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        trading_date_time = isoparse(d.pop("tradingDateTime"))

        instrument_identification_code_type = d.pop("instrumentIdentificationCodeType")

        instrument_identification_code = d.pop("instrumentIdentificationCode")

        price = d.pop("price")

        price_currency = d.pop("priceCurrency")

        price_notation = d.pop("priceNotation")

        quantity = d.pop("quantity")

        venue_of_execution = d.pop("venueOfExecution")

        publication_date_time = isoparse(d.pop("publicationDateTime"))

        transaction_identification_code = d.pop("transactionIdentificationCode")

        notional_amount = d.pop("notionalAmount")

        notional_currency = d.pop("notionalCurrency", UNSET)

        post_trade_transparency_data = cls(
            trading_date_time=trading_date_time,
            instrument_identification_code_type=instrument_identification_code_type,
            instrument_identification_code=instrument_identification_code,
            price=price,
            price_currency=price_currency,
            price_notation=price_notation,
            quantity=quantity,
            venue_of_execution=venue_of_execution,
            publication_date_time=publication_date_time,
            transaction_identification_code=transaction_identification_code,
            notional_amount=notional_amount,
            notional_currency=notional_currency,
        )

        post_trade_transparency_data.additional_properties = d
        return post_trade_transparency_data

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
