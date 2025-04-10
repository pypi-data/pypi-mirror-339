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

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, StrEnum

from x21_sdk.onchain import util


class OrderType(StrEnum):
    BUY = "Buy"
    SELL = "Sell"


class OrderBookPhase(Enum):
    NONE = 0
    OPEN_FOR_TRADING = 1
    CLOSED_FOR_TRADING = 2
    MANUAL_HALT = 3
    AUTOMATIC_HALT = 4


@dataclass
class Pair:
    base: Decimal = None
    quote: Decimal = None

    def __post_init__(self):
        self.base = util.to_decimal(self.base)
        self.quote = util.to_decimal(self.quote)


@dataclass
class OrderBookOrders:
    buy: list[Pair]
    sell: list[Pair]


@dataclass
class OrderBookOrderCount:
    buy: int
    sell: int


@dataclass
class PairConfiguration:
    base_scale: Decimal
    quote_scale: Decimal
    base_native_scale: Decimal
    quote_native_scale: Decimal
    maker_commission: int
    taker_commission: int
    market_maker_commission: int
    quote_token_address: str
    base_token_address: str
    whitelist_address: str
    commission_wallet: str
    base_token_fallback_wallet: str
    quote_token_fallback_wallet: str
    liquidity_band: int
    version: str

    base_internal_scale: Decimal = None
    quote_internal_scale: Decimal = None
    combined_internal_scale: Decimal = None

    def __post_init__(self):
        self.base_internal_scale = Decimal(self.base_native_scale) / Decimal(self.base_scale)
        self.quote_internal_scale = Decimal(self.quote_native_scale) / Decimal(self.quote_scale)
        self.combined_internal_scale = Decimal(self.base_internal_scale) * Decimal(self.quote_internal_scale)


@dataclass
class ClientInfo:
    id: int
    can_transfer: bool
    can_buy: bool
    can_sell: bool
    can_cancel: bool
    is_market_maker: bool


@dataclass
class PreTradeControlConfig:
    max_value: int
    min_value: int
    price_collar_factor: int
    max_matches: int


@dataclass
class VolatilityManagementConfig:
    static_threshold: int
    dynamic_threshold: int
