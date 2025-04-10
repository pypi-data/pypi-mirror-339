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


class CommodityDerivativesSubProductEnum(str, Enum):
    AMMO = "AMMO"
    CBRD = "CBRD"
    COAL = "COAL"
    CRBR = "CRBR"
    CSHP = "CSHP"
    CSTR = "CSTR"
    DAPH = "DAPH"
    DIRY = "DIRY"
    DIST = "DIST"
    DLVR = "DLVR"
    DRYF = "DRYF"
    ELEC = "ELEC"
    EMIS = "EMIS"
    FRST = "FRST"
    GRIN = "GRIN"
    GROS = "GROS"
    INRG = "INRG"
    LGHT = "LGHT"
    LSTK = "LSTK"
    MFTG = "MFTG"
    NDLV = "NDLV"
    NGAS = "NGAS"
    NPRM = "NPRM"
    NSPT = "NSPT"
    OILP = "OILP"
    OOLI = "OOLI"
    PLST = "PLST"
    POTA = "POTA"
    PRME = "PRME"
    PTSH = "PTSH"
    PULP = "PULP"
    RCVP = "RCVP"
    RNNG = "RNNG"
    SEAF = "SEAF"
    SLPH = "SLPH"
    SOFT = "SOFT"
    UAAN = "UAAN"
    UREA = "UREA"
    WETF = "WETF"
    WTHR = "WTHR"

    def __str__(self) -> str:
        return str(self.value)
