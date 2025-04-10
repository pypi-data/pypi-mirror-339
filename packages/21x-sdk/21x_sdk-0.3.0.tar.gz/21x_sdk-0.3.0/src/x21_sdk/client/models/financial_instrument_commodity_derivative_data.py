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

from ..models.commodity_derivative_final_price_type_enum import CommodityDerivativeFinalPriceTypeEnum
from ..models.commodity_derivative_size_specification_enum import CommodityDerivativeSizeSpecificationEnum
from ..models.commodity_derivative_transaction_type_enum import CommodityDerivativeTransactionTypeEnum
from ..models.commodity_derivatives_further_sub_product_enum import CommodityDerivativesFurtherSubProductEnum
from ..models.commodity_derivatives_product_enum import CommodityDerivativesProductEnum
from ..models.commodity_derivatives_sub_product_enum import CommodityDerivativesSubProductEnum
from ..models.emission_allowance_sub_type_enum import EmissionAllowanceSubTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentCommodityDerivativeData")


@_attrs_define
class FinancialInstrumentCommodityDerivativeData:
    """
    Attributes:
        base_product (Union[Unset, CommodityDerivativesProductEnum]):
        sub_product (Union[Unset, CommodityDerivativesSubProductEnum]):
        further_sub_product (Union[Unset, CommodityDerivativesFurtherSubProductEnum]):
        transaction_type (Union[Unset, CommodityDerivativeTransactionTypeEnum]):
        final_price_type (Union[Unset, CommodityDerivativeFinalPriceTypeEnum]):
        size_specification (Union[Unset, CommodityDerivativeSizeSpecificationEnum]):
        freight_route (Union[Unset, str]):
        settlement_location (Union[Unset, str]):
        commodity_notional_currency (Union[Unset, str]):
        emission_allowance_sub_type (Union[Unset, EmissionAllowanceSubTypeEnum]):
    """

    base_product: Union[Unset, CommodityDerivativesProductEnum] = UNSET
    sub_product: Union[Unset, CommodityDerivativesSubProductEnum] = UNSET
    further_sub_product: Union[Unset, CommodityDerivativesFurtherSubProductEnum] = UNSET
    transaction_type: Union[Unset, CommodityDerivativeTransactionTypeEnum] = UNSET
    final_price_type: Union[Unset, CommodityDerivativeFinalPriceTypeEnum] = UNSET
    size_specification: Union[Unset, CommodityDerivativeSizeSpecificationEnum] = UNSET
    freight_route: Union[Unset, str] = UNSET
    settlement_location: Union[Unset, str] = UNSET
    commodity_notional_currency: Union[Unset, str] = UNSET
    emission_allowance_sub_type: Union[Unset, EmissionAllowanceSubTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_product: Union[Unset, str] = UNSET
        if not isinstance(self.base_product, Unset):
            base_product = self.base_product.value

        sub_product: Union[Unset, str] = UNSET
        if not isinstance(self.sub_product, Unset):
            sub_product = self.sub_product.value

        further_sub_product: Union[Unset, str] = UNSET
        if not isinstance(self.further_sub_product, Unset):
            further_sub_product = self.further_sub_product.value

        transaction_type: Union[Unset, str] = UNSET
        if not isinstance(self.transaction_type, Unset):
            transaction_type = self.transaction_type.value

        final_price_type: Union[Unset, str] = UNSET
        if not isinstance(self.final_price_type, Unset):
            final_price_type = self.final_price_type.value

        size_specification: Union[Unset, str] = UNSET
        if not isinstance(self.size_specification, Unset):
            size_specification = self.size_specification.value

        freight_route = self.freight_route

        settlement_location = self.settlement_location

        commodity_notional_currency = self.commodity_notional_currency

        emission_allowance_sub_type: Union[Unset, str] = UNSET
        if not isinstance(self.emission_allowance_sub_type, Unset):
            emission_allowance_sub_type = self.emission_allowance_sub_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_product is not UNSET:
            field_dict["baseProduct"] = base_product
        if sub_product is not UNSET:
            field_dict["subProduct"] = sub_product
        if further_sub_product is not UNSET:
            field_dict["furtherSubProduct"] = further_sub_product
        if transaction_type is not UNSET:
            field_dict["transactionType"] = transaction_type
        if final_price_type is not UNSET:
            field_dict["finalPriceType"] = final_price_type
        if size_specification is not UNSET:
            field_dict["sizeSpecification"] = size_specification
        if freight_route is not UNSET:
            field_dict["freightRoute"] = freight_route
        if settlement_location is not UNSET:
            field_dict["settlementLocation"] = settlement_location
        if commodity_notional_currency is not UNSET:
            field_dict["commodityNotionalCurrency"] = commodity_notional_currency
        if emission_allowance_sub_type is not UNSET:
            field_dict["emissionAllowanceSubType"] = emission_allowance_sub_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _base_product = d.pop("baseProduct", UNSET)
        base_product: Union[Unset, CommodityDerivativesProductEnum]
        if isinstance(_base_product, Unset):
            base_product = UNSET
        else:
            base_product = CommodityDerivativesProductEnum(_base_product)

        _sub_product = d.pop("subProduct", UNSET)
        sub_product: Union[Unset, CommodityDerivativesSubProductEnum]
        if isinstance(_sub_product, Unset):
            sub_product = UNSET
        else:
            sub_product = CommodityDerivativesSubProductEnum(_sub_product)

        _further_sub_product = d.pop("furtherSubProduct", UNSET)
        further_sub_product: Union[Unset, CommodityDerivativesFurtherSubProductEnum]
        if isinstance(_further_sub_product, Unset):
            further_sub_product = UNSET
        else:
            further_sub_product = CommodityDerivativesFurtherSubProductEnum(_further_sub_product)

        _transaction_type = d.pop("transactionType", UNSET)
        transaction_type: Union[Unset, CommodityDerivativeTransactionTypeEnum]
        if isinstance(_transaction_type, Unset):
            transaction_type = UNSET
        else:
            transaction_type = CommodityDerivativeTransactionTypeEnum(_transaction_type)

        _final_price_type = d.pop("finalPriceType", UNSET)
        final_price_type: Union[Unset, CommodityDerivativeFinalPriceTypeEnum]
        if isinstance(_final_price_type, Unset):
            final_price_type = UNSET
        else:
            final_price_type = CommodityDerivativeFinalPriceTypeEnum(_final_price_type)

        _size_specification = d.pop("sizeSpecification", UNSET)
        size_specification: Union[Unset, CommodityDerivativeSizeSpecificationEnum]
        if isinstance(_size_specification, Unset):
            size_specification = UNSET
        else:
            size_specification = CommodityDerivativeSizeSpecificationEnum(_size_specification)

        freight_route = d.pop("freightRoute", UNSET)

        settlement_location = d.pop("settlementLocation", UNSET)

        commodity_notional_currency = d.pop("commodityNotionalCurrency", UNSET)

        _emission_allowance_sub_type = d.pop("emissionAllowanceSubType", UNSET)
        emission_allowance_sub_type: Union[Unset, EmissionAllowanceSubTypeEnum]
        if isinstance(_emission_allowance_sub_type, Unset):
            emission_allowance_sub_type = UNSET
        else:
            emission_allowance_sub_type = EmissionAllowanceSubTypeEnum(_emission_allowance_sub_type)

        financial_instrument_commodity_derivative_data = cls(
            base_product=base_product,
            sub_product=sub_product,
            further_sub_product=further_sub_product,
            transaction_type=transaction_type,
            final_price_type=final_price_type,
            size_specification=size_specification,
            freight_route=freight_route,
            settlement_location=settlement_location,
            commodity_notional_currency=commodity_notional_currency,
            emission_allowance_sub_type=emission_allowance_sub_type,
        )

        financial_instrument_commodity_derivative_data.additional_properties = d
        return financial_instrument_commodity_derivative_data

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
