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

from ..models.financial_instrument_index_term_unit_enum import FinancialInstrumentIndexTermUnitEnum
from ..models.index_definition_enum import IndexDefinitionEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentUnderlyingInstrumentData")


@_attrs_define
class FinancialInstrumentUnderlyingInstrumentData:
    """
    Attributes:
        isin (Union[Unset, str]):
        issuer_lei (Union[Unset, str]):
        index (Union[Unset, IndexDefinitionEnum]):
        index_name (Union[Unset, str]):
        index_term_unit (Union[Unset, FinancialInstrumentIndexTermUnitEnum]):
        index_term_value (Union[Unset, int]):
    """

    isin: Union[Unset, str] = UNSET
    issuer_lei: Union[Unset, str] = UNSET
    index: Union[Unset, IndexDefinitionEnum] = UNSET
    index_name: Union[Unset, str] = UNSET
    index_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum] = UNSET
    index_term_value: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        isin = self.isin

        issuer_lei = self.issuer_lei

        index: Union[Unset, str] = UNSET
        if not isinstance(self.index, Unset):
            index = self.index.value

        index_name = self.index_name

        index_term_unit: Union[Unset, str] = UNSET
        if not isinstance(self.index_term_unit, Unset):
            index_term_unit = self.index_term_unit.value

        index_term_value = self.index_term_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if isin is not UNSET:
            field_dict["isin"] = isin
        if issuer_lei is not UNSET:
            field_dict["issuerLei"] = issuer_lei
        if index is not UNSET:
            field_dict["index"] = index
        if index_name is not UNSET:
            field_dict["indexName"] = index_name
        if index_term_unit is not UNSET:
            field_dict["indexTermUnit"] = index_term_unit
        if index_term_value is not UNSET:
            field_dict["indexTermValue"] = index_term_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        isin = d.pop("isin", UNSET)

        issuer_lei = d.pop("issuerLei", UNSET)

        _index = d.pop("index", UNSET)
        index: Union[Unset, IndexDefinitionEnum]
        if isinstance(_index, Unset):
            index = UNSET
        else:
            index = IndexDefinitionEnum(_index)

        index_name = d.pop("indexName", UNSET)

        _index_term_unit = d.pop("indexTermUnit", UNSET)
        index_term_unit: Union[Unset, FinancialInstrumentIndexTermUnitEnum]
        if isinstance(_index_term_unit, Unset):
            index_term_unit = UNSET
        else:
            index_term_unit = FinancialInstrumentIndexTermUnitEnum(_index_term_unit)

        index_term_value = d.pop("indexTermValue", UNSET)

        financial_instrument_underlying_instrument_data = cls(
            isin=isin,
            issuer_lei=issuer_lei,
            index=index,
            index_name=index_name,
            index_term_unit=index_term_unit,
            index_term_value=index_term_value,
        )

        financial_instrument_underlying_instrument_data.additional_properties = d
        return financial_instrument_underlying_instrument_data

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
