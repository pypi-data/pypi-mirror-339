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
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.web_socket_order_book_data_item import WebSocketOrderBookDataItem


T = TypeVar("T", bound="WebSocketOrderBookFull")


@_attrs_define
class WebSocketOrderBookFull:
    """
    Attributes:
        channel (Union[Unset, str]):
        type_ (Union[Unset, str]):
        data (Union[Unset, list['WebSocketOrderBookDataItem']]):
    """

    channel: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    data: Union[Unset, list["WebSocketOrderBookDataItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel = self.channel

        type_ = self.type_

        data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channel is not UNSET:
            field_dict["channel"] = channel
        if type_ is not UNSET:
            field_dict["type"] = type_
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.web_socket_order_book_data_item import WebSocketOrderBookDataItem

        d = dict(src_dict)
        channel = d.pop("channel", UNSET)

        type_ = d.pop("type", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = WebSocketOrderBookDataItem.from_dict(data_item_data)

            data.append(data_item)

        web_socket_order_book_full = cls(
            channel=channel,
            type_=type_,
            data=data,
        )

        web_socket_order_book_full.additional_properties = d
        return web_socket_order_book_full

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
