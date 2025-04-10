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


class OrderStatusReasonEnum(str, Enum):
    ADMIN_CANCEL = "ADMIN_CANCEL"
    AUTHORITY_REQUEST = "AUTHORITY_REQUEST"
    CREATOR_CANCEL = "CREATOR_CANCEL"
    EXECUTED_SUCCESSFULLY = "EXECUTED_SUCCESSFULLY"
    EXECUTION_CONDITION_BOC = "EXECUTION_CONDITION_BOC"
    EXECUTION_CONDITION_FOK = "EXECUTION_CONDITION_FOK"
    EXECUTION_CONDITION_IOC = "EXECUTION_CONDITION_IOC"
    LOWER_DYNAMIC_PRICE_RANGE = "LOWER_DYNAMIC_PRICE_RANGE"
    LOWER_STATIC_PRICE_RANGE = "LOWER_STATIC_PRICE_RANGE"
    MARKET_CLOSE = "MARKET_CLOSE"
    MAXIMUM_VALUE = "MAXIMUM_VALUE"
    MAXIMUM_VOLUME = "MAXIMUM_VOLUME"
    MINIMUM_VALUE = "MINIMUM_VALUE"
    MINIMUM_VOLUME = "MINIMUM_VOLUME"
    N_A = "N_A"
    OTHER = "OTHER"
    PARTICIPANT_REQUEST = "PARTICIPANT_REQUEST"
    PRICE_COLLAR = "PRICE_COLLAR"
    SELF_TRADE = "SELF_TRADE"
    TICK_SIZE_VIOLATION = "TICK_SIZE_VIOLATION"
    TOO_MANY_MATCHES = "TOO_MANY_MATCHES"
    UPPER_DYNAMIC_PRICE_RANGE = "UPPER_DYNAMIC_PRICE_RANGE"
    UPPER_STATIC_PRICE_RANGE = "UPPER_STATIC_PRICE_RANGE"
    VENUE_REQUEST = "VENUE_REQUEST"

    def __str__(self) -> str:
        return str(self.value)
