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


class FinancialInstrumentAssetTypeEnum(str, Enum):
    C_COLLECTIVE_INVESTMENT_VEHICLES = "C_COLLECTIVE_INVESTMENT_VEHICLES"
    D_DEBT_INSTRUMENTS = "D_DEBT_INSTRUMENTS"
    E_EQUITIES = "E_EQUITIES"
    F_FUTURES = "F_FUTURES"
    H_NON_LISTED_COMPLEX_OPTIONS = "H_NON_LISTED_COMPLEX_OPTIONS"
    I_SPOT = "I_SPOT"
    J_FORWARDS = "J_FORWARDS"
    O_LISTED_OPTIONS = "O_LISTED_OPTIONS"
    R_ENTITLEMENT = "R_ENTITLEMENT"
    S_SWAPS = "S_SWAPS"

    def __str__(self) -> str:
        return str(self.value)
