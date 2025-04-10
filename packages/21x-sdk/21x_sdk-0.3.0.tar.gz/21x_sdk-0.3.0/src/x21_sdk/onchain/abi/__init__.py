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

import json
import pathlib

orderbook_abi = {}
token_abi = {}
whitelist_abi = {}

_folder = pathlib.Path(__file__).parent.resolve()

with open(_folder / "orderbook.json", encoding="utf-8") as f:
    orderbook_abi = json.load(f)

with open(_folder / "token.json", encoding="utf-8") as f:
    token_abi = json.load(f)

with open(_folder / "whitelist.json", encoding="utf-8") as f:
    whitelist_abi = json.load(f)
