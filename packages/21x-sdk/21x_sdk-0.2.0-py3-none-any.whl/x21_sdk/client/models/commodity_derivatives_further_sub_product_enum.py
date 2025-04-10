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


class CommodityDerivativesFurtherSubProductEnum(str, Enum):
    ALUA = "ALUA"
    ALUM = "ALUM"
    BAKK = "BAKK"
    BDSL = "BDSL"
    BRNT = "BRNT"
    BRNX = "BRNX"
    BRWN = "BRWN"
    BSLD = "BSLD"
    CBLT = "CBLT"
    CCOA = "CCOA"
    CERE = "CERE"
    CNDA = "CNDA"
    COND = "COND"
    COPR = "COPR"
    CORN = "CORN"
    DBCR = "DBCR"
    DSEL = "DSEL"
    DUBA = "DUBA"
    ERUE = "ERUE"
    ESPO = "ESPO"
    ETHA = "ETHA"
    EUAA = "EUAA"
    EUAE = "EUAE"
    FITR = "FITR"
    FOIL = "FOIL"
    FUEL = "FUEL"
    FWHT = "FWHT"
    GASP = "GASP"
    GOIL = "GOIL"
    GOLD = "GOLD"
    GSLN = "GSLN"
    HEAT = "HEAT"
    IRON = "IRON"
    JTFL = "JTFL"
    KERO = "KERO"
    LAMP = "LAMP"
    LEAD = "LEAD"
    LLSO = "LLSO"
    LNGG = "LNGG"
    MARS = "MARS"
    MOLY = "MOLY"
    MWHT = "MWHT"
    NAPH = "NAPH"
    NASC = "NASC"
    NBPG = "NBPG"
    NCGG = "NCGG"
    NGLO = "NGLO"
    NICK = "NICK"
    OFFP = "OFFP"
    OTHR = "OTHR"
    PKLD = "PKLD"
    PLDM = "PLDM"
    PTNM = "PTNM"
    RICE = "RICE"
    ROBU = "ROBU"
    RPSD = "RPSD"
    SLVR = "SLVR"
    SOYB = "SOYB"
    STEL = "STEL"
    TAPI = "TAPI"
    TINN = "TINN"
    TNKR = "TNKR"
    TTFG = "TTFG"
    URAL = "URAL"
    WHSG = "WHSG"
    WTIO = "WTIO"
    ZINC = "ZINC"

    def __str__(self) -> str:
        return str(self.value)
