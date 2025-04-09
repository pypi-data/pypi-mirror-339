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

from enum import Enum


class TradingStatusChangeReasonEnum(str, Enum):
    AUTOMATIC_RESUME = "AUTOMATIC_RESUME"
    CAPACITY_LIMIT_HALT = "CAPACITY_LIMIT_HALT"
    END_OF_TRADING_DAY = "END_OF_TRADING_DAY"
    MANUAL_MARKET_CLOSE = "MANUAL_MARKET_CLOSE"
    MANUAL_MARKET_OPEN = "MANUAL_MARKET_OPEN"
    PARTICIPANT_INITIATED_HALT = "PARTICIPANT_INITIATED_HALT"
    REGULATOR_INITIATED_HALT = "REGULATOR_INITIATED_HALT"
    START_OF_TRADING_DAY = "START_OF_TRADING_DAY"
    TECHNICAL_HALT = "TECHNICAL_HALT"
    TRADING_PAIR_ACTIVATION = "TRADING_PAIR_ACTIVATION"
    TRADING_PAIR_CREATION = "TRADING_PAIR_CREATION"
    TRADING_PAIR_DEACTIVATION = "TRADING_PAIR_DEACTIVATION"
    TRADING_PAIR_OFFBOARDING = "TRADING_PAIR_OFFBOARDING"
    VENUE_INITIATED_HALT = "VENUE_INITIATED_HALT"
    VOLATILITY_HALT = "VOLATILITY_HALT"

    def __str__(self) -> str:
        return str(self.value)
