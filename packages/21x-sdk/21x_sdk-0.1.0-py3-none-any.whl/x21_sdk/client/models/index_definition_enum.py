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


class IndexDefinitionEnum(str, Enum):
    BBSW = "BBSW"
    BUBO = "BUBO"
    CDOR = "CDOR"
    CIBO = "CIBO"
    EONA = "EONA"
    EONS = "EONS"
    EUCH = "EUCH"
    EURI = "EURI"
    EUUS = "EUUS"
    FUSW = "FUSW"
    GCFR = "GCFR"
    ISDA = "ISDA"
    JIBA = "JIBA"
    LIBI = "LIBI"
    LIBO = "LIBO"
    MAAA = "MAAA"
    MOSP = "MOSP"
    NIBO = "NIBO"
    OTHR = "OTHR"
    PFAN = "PFAN"
    PRBO = "PRBO"
    STBO = "STBO"
    SWAP = "SWAP"
    TIBO = "TIBO"
    TLBO = "TLBO"
    TREA = "TREA"
    WIBO = "WIBO"

    def __str__(self) -> str:
        return str(self.value)
