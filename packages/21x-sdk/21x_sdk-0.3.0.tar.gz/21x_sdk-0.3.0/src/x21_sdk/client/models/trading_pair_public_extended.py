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

from ..models.block_chain_enum import BlockChainEnum
from ..models.trading_status_change_reason_enum import TradingStatusChangeReasonEnum
from ..models.trading_status_enum import TradingStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.financial_instrument_public import FinancialInstrumentPublic


T = TypeVar("T", bound="TradingPairPublicExtended")


@_attrs_define
class TradingPairPublicExtended:
    """
    Attributes:
        quote_token_symbol (str): The symbol of the e-money token that the financial instrument is traded in
        smart_contract_order_book (str): The blockchain address of the order book smart contract. Orders need to be sent
            to this address.
        smart_contract_base (str): The blockchain address of the financial instrument token smart contract.
        smart_contract_quote (str): The blockchain address of the e-money token smart contract.
        base_token_native_scale (str):
        quote_token_native_scale (str):
        base_token_internal_scale (str):
        quote_token_internal_scale (str):
        quote_token_equivalent_currency (str):
        creation_date (Union[Unset, datetime.datetime]):
        modification_date (Union[Unset, datetime.datetime]):
        minimum_size_increment (Union[Unset, str]): Smallest valid order size increment. All order sizes must be
            minimumTradeVolume + x*minimumSizeIncrement
        price_collar_factor (Union[Unset, int]): The price collar factor is used for pre-trade controls to determine the
            minimum and maximum limit price allowed.
        maximum_matches (Union[Unset, int]): The maximum number of standing orders in the order book that an incoming
            order can be matched with.
        static_threshold (Union[Unset, int]): The percentage range around the static reference price that the execution
            price must have (in base points)
        dynamic_threshold (Union[Unset, int]): The percentage range around the dynamic reference price that the
            execution price must have (in base points)
        liquidity_band (Union[Unset, int]): The liquidity band used for tick size checks
        block_chain (Union[Unset, BlockChainEnum]):
        maker_commission (Union[Unset, int]): Maker commission in base points (10^-4)
        taker_commission (Union[Unset, int]): Taker commission in base points (10^-4)
        market_maker_commission (Union[Unset, int]): Market maker commission in base points (10^-4)
        trading_status (Union[Unset, TradingStatusEnum]):
        order_book_version (Union[Unset, str]):
        status_change_reason (Union[Unset, TradingStatusChangeReasonEnum]):
        status_change_reason_text (Union[Unset, str]): Reason why the last status change was made (free text)
        static_reference_price (Union[Unset, str]): The static reference price. Updated automatically after each trading
            day.
        minimum_order_value (Union[Unset, str]): The minimum value (in quote tokens) that a valid order must have.
        maximum_order_value (Union[Unset, str]): The maximum value (in quote tokens) that a valid order can have.
        base_token_data (Union[Unset, FinancialInstrumentPublic]):
    """

    quote_token_symbol: str
    smart_contract_order_book: str
    smart_contract_base: str
    smart_contract_quote: str
    base_token_native_scale: str
    quote_token_native_scale: str
    base_token_internal_scale: str
    quote_token_internal_scale: str
    quote_token_equivalent_currency: str
    creation_date: Union[Unset, datetime.datetime] = UNSET
    modification_date: Union[Unset, datetime.datetime] = UNSET
    minimum_size_increment: Union[Unset, str] = UNSET
    price_collar_factor: Union[Unset, int] = UNSET
    maximum_matches: Union[Unset, int] = UNSET
    static_threshold: Union[Unset, int] = UNSET
    dynamic_threshold: Union[Unset, int] = UNSET
    liquidity_band: Union[Unset, int] = UNSET
    block_chain: Union[Unset, BlockChainEnum] = UNSET
    maker_commission: Union[Unset, int] = UNSET
    taker_commission: Union[Unset, int] = UNSET
    market_maker_commission: Union[Unset, int] = UNSET
    trading_status: Union[Unset, TradingStatusEnum] = UNSET
    order_book_version: Union[Unset, str] = UNSET
    status_change_reason: Union[Unset, TradingStatusChangeReasonEnum] = UNSET
    status_change_reason_text: Union[Unset, str] = UNSET
    static_reference_price: Union[Unset, str] = UNSET
    minimum_order_value: Union[Unset, str] = UNSET
    maximum_order_value: Union[Unset, str] = UNSET
    base_token_data: Union[Unset, "FinancialInstrumentPublic"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        quote_token_symbol = self.quote_token_symbol

        smart_contract_order_book = self.smart_contract_order_book

        smart_contract_base = self.smart_contract_base

        smart_contract_quote = self.smart_contract_quote

        base_token_native_scale = self.base_token_native_scale

        quote_token_native_scale = self.quote_token_native_scale

        base_token_internal_scale = self.base_token_internal_scale

        quote_token_internal_scale = self.quote_token_internal_scale

        quote_token_equivalent_currency = self.quote_token_equivalent_currency

        creation_date: Union[Unset, str] = UNSET
        if not isinstance(self.creation_date, Unset):
            creation_date = self.creation_date.isoformat()

        modification_date: Union[Unset, str] = UNSET
        if not isinstance(self.modification_date, Unset):
            modification_date = self.modification_date.isoformat()

        minimum_size_increment = self.minimum_size_increment

        price_collar_factor = self.price_collar_factor

        maximum_matches = self.maximum_matches

        static_threshold = self.static_threshold

        dynamic_threshold = self.dynamic_threshold

        liquidity_band = self.liquidity_band

        block_chain: Union[Unset, str] = UNSET
        if not isinstance(self.block_chain, Unset):
            block_chain = self.block_chain.value

        maker_commission = self.maker_commission

        taker_commission = self.taker_commission

        market_maker_commission = self.market_maker_commission

        trading_status: Union[Unset, str] = UNSET
        if not isinstance(self.trading_status, Unset):
            trading_status = self.trading_status.value

        order_book_version = self.order_book_version

        status_change_reason: Union[Unset, str] = UNSET
        if not isinstance(self.status_change_reason, Unset):
            status_change_reason = self.status_change_reason.value

        status_change_reason_text = self.status_change_reason_text

        static_reference_price = self.static_reference_price

        minimum_order_value = self.minimum_order_value

        maximum_order_value = self.maximum_order_value

        base_token_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.base_token_data, Unset):
            base_token_data = self.base_token_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "quoteTokenSymbol": quote_token_symbol,
                "smartContractOrderBook": smart_contract_order_book,
                "smartContractBase": smart_contract_base,
                "smartContractQuote": smart_contract_quote,
                "baseTokenNativeScale": base_token_native_scale,
                "quoteTokenNativeScale": quote_token_native_scale,
                "baseTokenInternalScale": base_token_internal_scale,
                "quoteTokenInternalScale": quote_token_internal_scale,
                "quoteTokenEquivalentCurrency": quote_token_equivalent_currency,
            }
        )
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if modification_date is not UNSET:
            field_dict["modificationDate"] = modification_date
        if minimum_size_increment is not UNSET:
            field_dict["minimumSizeIncrement"] = minimum_size_increment
        if price_collar_factor is not UNSET:
            field_dict["priceCollarFactor"] = price_collar_factor
        if maximum_matches is not UNSET:
            field_dict["maximumMatches"] = maximum_matches
        if static_threshold is not UNSET:
            field_dict["staticThreshold"] = static_threshold
        if dynamic_threshold is not UNSET:
            field_dict["dynamicThreshold"] = dynamic_threshold
        if liquidity_band is not UNSET:
            field_dict["liquidityBand"] = liquidity_band
        if block_chain is not UNSET:
            field_dict["blockChain"] = block_chain
        if maker_commission is not UNSET:
            field_dict["makerCommission"] = maker_commission
        if taker_commission is not UNSET:
            field_dict["takerCommission"] = taker_commission
        if market_maker_commission is not UNSET:
            field_dict["marketMakerCommission"] = market_maker_commission
        if trading_status is not UNSET:
            field_dict["tradingStatus"] = trading_status
        if order_book_version is not UNSET:
            field_dict["orderBookVersion"] = order_book_version
        if status_change_reason is not UNSET:
            field_dict["statusChangeReason"] = status_change_reason
        if status_change_reason_text is not UNSET:
            field_dict["statusChangeReasonText"] = status_change_reason_text
        if static_reference_price is not UNSET:
            field_dict["staticReferencePrice"] = static_reference_price
        if minimum_order_value is not UNSET:
            field_dict["minimumOrderValue"] = minimum_order_value
        if maximum_order_value is not UNSET:
            field_dict["maximumOrderValue"] = maximum_order_value
        if base_token_data is not UNSET:
            field_dict["baseTokenData"] = base_token_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.financial_instrument_public import FinancialInstrumentPublic

        d = dict(src_dict)
        quote_token_symbol = d.pop("quoteTokenSymbol")

        smart_contract_order_book = d.pop("smartContractOrderBook")

        smart_contract_base = d.pop("smartContractBase")

        smart_contract_quote = d.pop("smartContractQuote")

        base_token_native_scale = d.pop("baseTokenNativeScale")

        quote_token_native_scale = d.pop("quoteTokenNativeScale")

        base_token_internal_scale = d.pop("baseTokenInternalScale")

        quote_token_internal_scale = d.pop("quoteTokenInternalScale")

        quote_token_equivalent_currency = d.pop("quoteTokenEquivalentCurrency")

        _creation_date = d.pop("creationDate", UNSET)
        creation_date: Union[Unset, datetime.datetime]
        if isinstance(_creation_date, Unset):
            creation_date = UNSET
        else:
            creation_date = isoparse(_creation_date)

        _modification_date = d.pop("modificationDate", UNSET)
        modification_date: Union[Unset, datetime.datetime]
        if isinstance(_modification_date, Unset):
            modification_date = UNSET
        else:
            modification_date = isoparse(_modification_date)

        minimum_size_increment = d.pop("minimumSizeIncrement", UNSET)

        price_collar_factor = d.pop("priceCollarFactor", UNSET)

        maximum_matches = d.pop("maximumMatches", UNSET)

        static_threshold = d.pop("staticThreshold", UNSET)

        dynamic_threshold = d.pop("dynamicThreshold", UNSET)

        liquidity_band = d.pop("liquidityBand", UNSET)

        _block_chain = d.pop("blockChain", UNSET)
        block_chain: Union[Unset, BlockChainEnum]
        if isinstance(_block_chain, Unset):
            block_chain = UNSET
        else:
            block_chain = BlockChainEnum(_block_chain)

        maker_commission = d.pop("makerCommission", UNSET)

        taker_commission = d.pop("takerCommission", UNSET)

        market_maker_commission = d.pop("marketMakerCommission", UNSET)

        _trading_status = d.pop("tradingStatus", UNSET)
        trading_status: Union[Unset, TradingStatusEnum]
        if isinstance(_trading_status, Unset):
            trading_status = UNSET
        else:
            trading_status = TradingStatusEnum(_trading_status)

        order_book_version = d.pop("orderBookVersion", UNSET)

        _status_change_reason = d.pop("statusChangeReason", UNSET)
        status_change_reason: Union[Unset, TradingStatusChangeReasonEnum]
        if isinstance(_status_change_reason, Unset):
            status_change_reason = UNSET
        else:
            status_change_reason = TradingStatusChangeReasonEnum(_status_change_reason)

        status_change_reason_text = d.pop("statusChangeReasonText", UNSET)

        static_reference_price = d.pop("staticReferencePrice", UNSET)

        minimum_order_value = d.pop("minimumOrderValue", UNSET)

        maximum_order_value = d.pop("maximumOrderValue", UNSET)

        _base_token_data = d.pop("baseTokenData", UNSET)
        base_token_data: Union[Unset, FinancialInstrumentPublic]
        if isinstance(_base_token_data, Unset):
            base_token_data = UNSET
        else:
            base_token_data = FinancialInstrumentPublic.from_dict(_base_token_data)

        trading_pair_public_extended = cls(
            quote_token_symbol=quote_token_symbol,
            smart_contract_order_book=smart_contract_order_book,
            smart_contract_base=smart_contract_base,
            smart_contract_quote=smart_contract_quote,
            base_token_native_scale=base_token_native_scale,
            quote_token_native_scale=quote_token_native_scale,
            base_token_internal_scale=base_token_internal_scale,
            quote_token_internal_scale=quote_token_internal_scale,
            quote_token_equivalent_currency=quote_token_equivalent_currency,
            creation_date=creation_date,
            modification_date=modification_date,
            minimum_size_increment=minimum_size_increment,
            price_collar_factor=price_collar_factor,
            maximum_matches=maximum_matches,
            static_threshold=static_threshold,
            dynamic_threshold=dynamic_threshold,
            liquidity_band=liquidity_band,
            block_chain=block_chain,
            maker_commission=maker_commission,
            taker_commission=taker_commission,
            market_maker_commission=market_maker_commission,
            trading_status=trading_status,
            order_book_version=order_book_version,
            status_change_reason=status_change_reason,
            status_change_reason_text=status_change_reason_text,
            static_reference_price=static_reference_price,
            minimum_order_value=minimum_order_value,
            maximum_order_value=maximum_order_value,
            base_token_data=base_token_data,
        )

        trading_pair_public_extended.additional_properties = d
        return trading_pair_public_extended

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
