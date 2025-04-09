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


class FinancialInstrumentAssetSubtypeEnum(str, Enum):
    C_B = "C_B"
    C_E = "C_E"
    C_F = "C_F"
    C_H = "C_H"
    C_I = "C_I"
    C_M = "C_M"
    C_P = "C_P"
    C_S = "C_S"
    D_A = "D_A"
    D_B = "D_B"
    D_C = "D_C"
    D_D = "D_D"
    D_E = "D_E"
    D_G = "D_G"
    D_M = "D_M"
    D_N = "D_N"
    D_S = "D_S"
    D_T = "D_T"
    D_W = "D_W"
    D_Y = "D_Y"
    E_C = "E_C"
    E_D = "E_D"
    E_F = "E_F"
    E_L = "E_L"
    E_M = "E_M"
    E_P = "E_P"
    E_S = "E_S"
    E_Y = "E_Y"
    F_C = "F_C"
    F_F = "F_F"
    H_C = "H_C"
    H_E = "H_E"
    H_F = "H_F"
    H_M = "H_M"
    H_R = "H_R"
    H_T = "H_T"
    I_F = "I_F"
    I_T = "I_T"
    J_C = "J_C"
    J_E = "J_E"
    J_F = "J_F"
    J_R = "J_R"
    J_T = "J_T"
    O_C = "O_C"
    O_M = "O_M"
    O_P = "O_P"
    R_A = "R_A"
    R_D = "R_D"
    R_F = "R_F"
    R_M = "R_M"
    R_P = "R_P"
    R_S = "R_S"
    R_W = "R_W"
    S_C = "S_C"
    S_E = "S_E"
    S_F = "S_F"
    S_M = "S_M"
    S_R = "S_R"
    S_T = "S_T"

    def __str__(self) -> str:
        return str(self.value)
