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

from ..models.order_kind_enum import OrderKindEnum
from ..models.order_quantity_type_enum import OrderQuantityTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.primary_market_order_data_additional_data import PrimaryMarketOrderDataAdditionalData


T = TypeVar("T", bound="PrimaryMarketOrderData")


@_attrs_define
class PrimaryMarketOrderData:
    """
    Attributes:
        order_kind (OrderKindEnum):
        financial_instrument_id (str): The ID of the financial instrument that shall be traded
        quantity (str): The number of financial instrument tokens that shall be traded
        quantity_type (OrderQuantityTypeEnum):
        timestamp (str): Time of order creation (in UTC time zone)
        price_limit (Union[Unset, str]): The price limit is optional since it is only applicable in some cases
        settlement_currency (Union[Unset, str]): The currency used for the price limit, and in which the trade should be
            settled
        additional_data (Union[Unset, PrimaryMarketOrderDataAdditionalData]): Arbitrary additional data to be added to
            the order information
    """

    order_kind: OrderKindEnum
    financial_instrument_id: str
    quantity: str
    quantity_type: OrderQuantityTypeEnum
    timestamp: str
    price_limit: Union[Unset, str] = UNSET
    settlement_currency: Union[Unset, str] = UNSET
    additional_data: Union[Unset, "PrimaryMarketOrderDataAdditionalData"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        order_kind = self.order_kind.value

        financial_instrument_id = self.financial_instrument_id

        quantity = self.quantity

        quantity_type = self.quantity_type.value

        timestamp = self.timestamp

        price_limit = self.price_limit

        settlement_currency = self.settlement_currency

        additional_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.additional_data, Unset):
            additional_data = self.additional_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "orderKind": order_kind,
                "financialInstrumentId": financial_instrument_id,
                "quantity": quantity,
                "quantityType": quantity_type,
                "timestamp": timestamp,
            }
        )
        if price_limit is not UNSET:
            field_dict["priceLimit"] = price_limit
        if settlement_currency is not UNSET:
            field_dict["settlementCurrency"] = settlement_currency
        if additional_data is not UNSET:
            field_dict["additionalData"] = additional_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.primary_market_order_data_additional_data import PrimaryMarketOrderDataAdditionalData

        d = dict(src_dict)
        order_kind = OrderKindEnum(d.pop("orderKind"))

        financial_instrument_id = d.pop("financialInstrumentId")

        quantity = d.pop("quantity")

        quantity_type = OrderQuantityTypeEnum(d.pop("quantityType"))

        timestamp = d.pop("timestamp")

        price_limit = d.pop("priceLimit", UNSET)

        settlement_currency = d.pop("settlementCurrency", UNSET)

        _additional_data = d.pop("additionalData", UNSET)
        additional_data: Union[Unset, PrimaryMarketOrderDataAdditionalData]
        if isinstance(_additional_data, Unset):
            additional_data = UNSET
        else:
            additional_data = PrimaryMarketOrderDataAdditionalData.from_dict(_additional_data)

        primary_market_order_data = cls(
            order_kind=order_kind,
            financial_instrument_id=financial_instrument_id,
            quantity=quantity,
            quantity_type=quantity_type,
            timestamp=timestamp,
            price_limit=price_limit,
            settlement_currency=settlement_currency,
            additional_data=additional_data,
        )

        primary_market_order_data.additional_properties = d
        return primary_market_order_data

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
