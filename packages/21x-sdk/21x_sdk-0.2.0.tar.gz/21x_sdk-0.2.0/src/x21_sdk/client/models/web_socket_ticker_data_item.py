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

T = TypeVar("T", bound="WebSocketTickerDataItem")


@_attrs_define
class WebSocketTickerDataItem:
    """
    Attributes:
        symbol (Union[Unset, str]):
        last_price (Union[Unset, str]):
        best_buy_limit (Union[Unset, str]):
        best_buy_quantity (Union[Unset, str]):
        best_sell_limit (Union[Unset, str]):
        best_sell_quantity (Union[Unset, str]):
        time (Union[Unset, datetime.datetime]):
    """

    symbol: Union[Unset, str] = UNSET
    last_price: Union[Unset, str] = UNSET
    best_buy_limit: Union[Unset, str] = UNSET
    best_buy_quantity: Union[Unset, str] = UNSET
    best_sell_limit: Union[Unset, str] = UNSET
    best_sell_quantity: Union[Unset, str] = UNSET
    time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        last_price = self.last_price

        best_buy_limit = self.best_buy_limit

        best_buy_quantity = self.best_buy_quantity

        best_sell_limit = self.best_sell_limit

        best_sell_quantity = self.best_sell_quantity

        time: Union[Unset, str] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if last_price is not UNSET:
            field_dict["lastPrice"] = last_price
        if best_buy_limit is not UNSET:
            field_dict["bestBuyLimit"] = best_buy_limit
        if best_buy_quantity is not UNSET:
            field_dict["bestBuyQuantity"] = best_buy_quantity
        if best_sell_limit is not UNSET:
            field_dict["bestSellLimit"] = best_sell_limit
        if best_sell_quantity is not UNSET:
            field_dict["bestSellQuantity"] = best_sell_quantity
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        symbol = d.pop("symbol", UNSET)

        last_price = d.pop("lastPrice", UNSET)

        best_buy_limit = d.pop("bestBuyLimit", UNSET)

        best_buy_quantity = d.pop("bestBuyQuantity", UNSET)

        best_sell_limit = d.pop("bestSellLimit", UNSET)

        best_sell_quantity = d.pop("bestSellQuantity", UNSET)

        _time = d.pop("time", UNSET)
        time: Union[Unset, datetime.datetime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        web_socket_ticker_data_item = cls(
            symbol=symbol,
            last_price=last_price,
            best_buy_limit=best_buy_limit,
            best_buy_quantity=best_buy_quantity,
            best_sell_limit=best_sell_limit,
            best_sell_quantity=best_sell_quantity,
            time=time,
        )

        web_socket_ticker_data_item.additional_properties = d
        return web_socket_ticker_data_item

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
