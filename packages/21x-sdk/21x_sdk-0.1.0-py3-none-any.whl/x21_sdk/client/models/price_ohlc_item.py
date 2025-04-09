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

from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PriceOhlcItem")


@_attrs_define
class PriceOhlcItem:
    """
    Attributes:
        x (Union[Unset, int]): Unix Timestamp
        o (Union[Unset, str]): Opening price
        h (Union[Unset, str]): Highest price
        l (Union[Unset, str]): Lowest price
        c (Union[Unset, str]): Closing price
    """

    x: Union[Unset, int] = UNSET
    o: Union[Unset, str] = UNSET
    h: Union[Unset, str] = UNSET
    l: Union[Unset, str] = UNSET
    c: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        x = self.x

        o = self.o

        h = self.h

        l = self.l

        c = self.c

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if x is not UNSET:
            field_dict["x"] = x
        if o is not UNSET:
            field_dict["o"] = o
        if h is not UNSET:
            field_dict["h"] = h
        if l is not UNSET:
            field_dict["l"] = l
        if c is not UNSET:
            field_dict["c"] = c

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        x = d.pop("x", UNSET)

        o = d.pop("o", UNSET)

        h = d.pop("h", UNSET)

        l = d.pop("l", UNSET)

        c = d.pop("c", UNSET)

        price_ohlc_item = cls(
            x=x,
            o=o,
            h=h,
            l=l,
            c=c,
        )

        price_ohlc_item.additional_properties = d
        return price_ohlc_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
