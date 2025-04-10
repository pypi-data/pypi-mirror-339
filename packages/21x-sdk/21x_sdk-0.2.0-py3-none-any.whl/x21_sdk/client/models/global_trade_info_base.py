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

from ..models.trading_status_change_reason_enum import TradingStatusChangeReasonEnum
from ..models.trading_status_enum import TradingStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalTradeInfoBase")


@_attrs_define
class GlobalTradeInfoBase:
    """
    Attributes:
        last_price (Union[Unset, str]): The price at which the last trade happened
        reference_price (Union[Unset, str]): The reference price is set to the price at the close of the previous
            trading day. Used for pre-trade controls.
        price_change_24_h (Union[Unset, str]):
        trade_volume_24_h (Union[Unset, str]):
        liquidity_band (Union[Unset, int]): The liquidity band used to validate limit prices (tick size check)
        trading_status (Union[Unset, TradingStatusEnum]):
        status_change_reason (Union[Unset, TradingStatusChangeReasonEnum]):
        status_change_reason_text (Union[Unset, str]): Reason why the last status change was made (free text)
        trading_halt_counter (Union[Unset, int]): The number of trading halts that have occurred on the current trading
            day
        estimated_trading_halt_end (Union[Unset, datetime.datetime]): If we are in a trading halt, the time when trading
            is expected to be resumed
    """

    last_price: Union[Unset, str] = UNSET
    reference_price: Union[Unset, str] = UNSET
    price_change_24_h: Union[Unset, str] = UNSET
    trade_volume_24_h: Union[Unset, str] = UNSET
    liquidity_band: Union[Unset, int] = UNSET
    trading_status: Union[Unset, TradingStatusEnum] = UNSET
    status_change_reason: Union[Unset, TradingStatusChangeReasonEnum] = UNSET
    status_change_reason_text: Union[Unset, str] = UNSET
    trading_halt_counter: Union[Unset, int] = UNSET
    estimated_trading_halt_end: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        last_price = self.last_price

        reference_price = self.reference_price

        price_change_24_h = self.price_change_24_h

        trade_volume_24_h = self.trade_volume_24_h

        liquidity_band = self.liquidity_band

        trading_status: Union[Unset, str] = UNSET
        if not isinstance(self.trading_status, Unset):
            trading_status = self.trading_status.value

        status_change_reason: Union[Unset, str] = UNSET
        if not isinstance(self.status_change_reason, Unset):
            status_change_reason = self.status_change_reason.value

        status_change_reason_text = self.status_change_reason_text

        trading_halt_counter = self.trading_halt_counter

        estimated_trading_halt_end: Union[Unset, str] = UNSET
        if not isinstance(self.estimated_trading_halt_end, Unset):
            estimated_trading_halt_end = self.estimated_trading_halt_end.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if last_price is not UNSET:
            field_dict["lastPrice"] = last_price
        if reference_price is not UNSET:
            field_dict["referencePrice"] = reference_price
        if price_change_24_h is not UNSET:
            field_dict["priceChange24h"] = price_change_24_h
        if trade_volume_24_h is not UNSET:
            field_dict["tradeVolume24h"] = trade_volume_24_h
        if liquidity_band is not UNSET:
            field_dict["liquidityBand"] = liquidity_band
        if trading_status is not UNSET:
            field_dict["tradingStatus"] = trading_status
        if status_change_reason is not UNSET:
            field_dict["statusChangeReason"] = status_change_reason
        if status_change_reason_text is not UNSET:
            field_dict["statusChangeReasonText"] = status_change_reason_text
        if trading_halt_counter is not UNSET:
            field_dict["tradingHaltCounter"] = trading_halt_counter
        if estimated_trading_halt_end is not UNSET:
            field_dict["estimatedTradingHaltEnd"] = estimated_trading_halt_end

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        last_price = d.pop("lastPrice", UNSET)

        reference_price = d.pop("referencePrice", UNSET)

        price_change_24_h = d.pop("priceChange24h", UNSET)

        trade_volume_24_h = d.pop("tradeVolume24h", UNSET)

        liquidity_band = d.pop("liquidityBand", UNSET)

        _trading_status = d.pop("tradingStatus", UNSET)
        trading_status: Union[Unset, TradingStatusEnum]
        if isinstance(_trading_status, Unset):
            trading_status = UNSET
        else:
            trading_status = TradingStatusEnum(_trading_status)

        _status_change_reason = d.pop("statusChangeReason", UNSET)
        status_change_reason: Union[Unset, TradingStatusChangeReasonEnum]
        if isinstance(_status_change_reason, Unset):
            status_change_reason = UNSET
        else:
            status_change_reason = TradingStatusChangeReasonEnum(_status_change_reason)

        status_change_reason_text = d.pop("statusChangeReasonText", UNSET)

        trading_halt_counter = d.pop("tradingHaltCounter", UNSET)

        _estimated_trading_halt_end = d.pop("estimatedTradingHaltEnd", UNSET)
        estimated_trading_halt_end: Union[Unset, datetime.datetime]
        if isinstance(_estimated_trading_halt_end, Unset):
            estimated_trading_halt_end = UNSET
        else:
            estimated_trading_halt_end = isoparse(_estimated_trading_halt_end)

        global_trade_info_base = cls(
            last_price=last_price,
            reference_price=reference_price,
            price_change_24_h=price_change_24_h,
            trade_volume_24_h=trade_volume_24_h,
            liquidity_band=liquidity_band,
            trading_status=trading_status,
            status_change_reason=status_change_reason,
            status_change_reason_text=status_change_reason_text,
            trading_halt_counter=trading_halt_counter,
            estimated_trading_halt_end=estimated_trading_halt_end,
        )

        global_trade_info_base.additional_properties = d
        return global_trade_info_base

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
