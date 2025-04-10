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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.order_book_price_level_item import OrderBookPriceLevelItem


T = TypeVar("T", bound="WebSocketOrderBookDataItem")


@_attrs_define
class WebSocketOrderBookDataItem:
    """
    Attributes:
        symbol (Union[Unset, str]):
        time (Union[Unset, datetime.datetime]):
        buy (Union[Unset, list['OrderBookPriceLevelItem']]):
        sell (Union[Unset, list['OrderBookPriceLevelItem']]):
    """

    symbol: Union[Unset, str] = UNSET
    time: Union[Unset, datetime.datetime] = UNSET
    buy: Union[Unset, list["OrderBookPriceLevelItem"]] = UNSET
    sell: Union[Unset, list["OrderBookPriceLevelItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        symbol = self.symbol

        time: Union[Unset, str] = UNSET
        if not isinstance(self.time, Unset):
            time = self.time.isoformat()

        buy: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.buy, Unset):
            buy = []
            for buy_item_data in self.buy:
                buy_item = buy_item_data.to_dict()
                buy.append(buy_item)

        sell: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sell, Unset):
            sell = []
            for sell_item_data in self.sell:
                sell_item = sell_item_data.to_dict()
                sell.append(sell_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if time is not UNSET:
            field_dict["time"] = time
        if buy is not UNSET:
            field_dict["buy"] = buy
        if sell is not UNSET:
            field_dict["sell"] = sell

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.order_book_price_level_item import OrderBookPriceLevelItem

        d = dict(src_dict)
        symbol = d.pop("symbol", UNSET)

        _time = d.pop("time", UNSET)
        time: Union[Unset, datetime.datetime]
        if isinstance(_time, Unset):
            time = UNSET
        else:
            time = isoparse(_time)

        buy = []
        _buy = d.pop("buy", UNSET)
        for buy_item_data in _buy or []:
            buy_item = OrderBookPriceLevelItem.from_dict(buy_item_data)

            buy.append(buy_item)

        sell = []
        _sell = d.pop("sell", UNSET)
        for sell_item_data in _sell or []:
            sell_item = OrderBookPriceLevelItem.from_dict(sell_item_data)

            sell.append(sell_item)

        web_socket_order_book_data_item = cls(
            symbol=symbol,
            time=time,
            buy=buy,
            sell=sell,
        )

        web_socket_order_book_data_item.additional_properties = d
        return web_socket_order_book_data_item

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
