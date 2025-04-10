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

from ..models.order_type_enum import OrderTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderBookItemReduced")


@_attrs_define
class OrderBookItemReduced:
    """
    Attributes:
        order_type (OrderTypeEnum):
        quantity (str): Remaining order size in financial instrument (base) tokens
        limit (Union[Unset, str]): The price limit of the order. Mandatory for limit orders
    """

    order_type: OrderTypeEnum
    quantity: str
    limit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order_type = self.order_type.value

        quantity = self.quantity

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "orderType": order_type,
                "quantity": quantity,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        order_type = OrderTypeEnum(d.pop("orderType"))

        quantity = d.pop("quantity")

        limit = d.pop("limit", UNSET)

        order_book_item_reduced = cls(
            order_type=order_type,
            quantity=quantity,
            limit=limit,
        )

        order_book_item_reduced.additional_properties = d
        return order_book_item_reduced

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
