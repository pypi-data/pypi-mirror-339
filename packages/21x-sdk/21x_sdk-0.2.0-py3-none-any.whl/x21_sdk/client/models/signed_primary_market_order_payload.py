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
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.primary_market_order_data import PrimaryMarketOrderData


T = TypeVar("T", bound="SignedPrimaryMarketOrderPayload")


@_attrs_define
class SignedPrimaryMarketOrderPayload:
    """
    Attributes:
        payload (PrimaryMarketOrderData):
        signature (str): Digital signature of the payload data, created by the sending wallet
    """

    payload: "PrimaryMarketOrderData"
    signature: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = self.payload.to_dict()

        signature = self.signature

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "payload": payload,
                "signature": signature,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.primary_market_order_data import PrimaryMarketOrderData

        d = dict(src_dict)
        payload = PrimaryMarketOrderData.from_dict(d.pop("payload"))

        signature = d.pop("signature")

        signed_primary_market_order_payload = cls(
            payload=payload,
            signature=signature,
        )

        signed_primary_market_order_payload.additional_properties = d
        return signed_primary_market_order_payload

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
