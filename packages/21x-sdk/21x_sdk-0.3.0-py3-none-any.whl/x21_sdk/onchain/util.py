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

from decimal import Decimal

LOWER64 = 2**64 - 1
LOWER128 = 2**128 - 1

# Define price ranges as tuples with (lower_bound, upper_bound) and store values for liquidity bands
TICKSIZE_TABLE = [
    ((0, 0.1), [0.0005, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001]),
    ((0.1, 0.2), [0.001, 0.0005, 0.0002, 0.0001, 0.0001, 0.0001]),
    ((0.2, 0.5), [0.002, 0.001, 0.0005, 0.0002, 0.0001, 0.0001]),
    ((0.5, 1), [0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]),
    ((1, 2), [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002]),
    ((2, 5), [0.02, 0.01, 0.005, 0.002, 0.001, 0.0005]),
    ((5, 10), [0.05, 0.02, 0.01, 0.005, 0.002, 0.001]),
    ((10, 20), [0.1, 0.05, 0.02, 0.01, 0.005, 0.002]),
    ((20, 50), [0.2, 0.1, 0.05, 0.02, 0.01, 0.005]),
    ((50, 100), [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]),
    ((100, 200), [1, 0.5, 0.2, 0.1, 0.05, 0.02]),
    ((200, 500), [2, 1, 0.5, 0.2, 0.1, 0.05]),
    ((500, 1000), [5, 2, 1, 0.5, 0.2, 0.1]),
    ((1000, 2000), [10, 5, 2, 1, 0.5, 0.2]),
    ((2000, 5000), [20, 10, 5, 2, 1, 0.5]),
    ((5000, 10000), [50, 20, 10, 5, 2, 1]),
    ((10000, 20000), [100, 50, 20, 10, 5, 2]),
    ((20000, 50000), [200, 100, 50, 20, 10, 5]),
    ((50000, float("inf")), [500, 200, 100, 50, 20, 10]),  # Last range is open-ended
]


def to_decimal(number: int | float | str) -> Decimal:
    """convert a number to a Decimal object"""
    return Decimal(str(number))


def convert_bytes_version_to_string(version: bytes) -> str:
    stripped_bytes = version.lstrip(b"\x00")
    return stripped_bytes.decode("utf-8")
