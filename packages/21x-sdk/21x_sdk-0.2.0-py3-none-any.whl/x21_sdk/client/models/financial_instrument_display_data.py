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

from ..models.financial_instrument_asset_subtype_enum import FinancialInstrumentAssetSubtypeEnum
from ..models.financial_instrument_asset_type_enum import FinancialInstrumentAssetTypeEnum
from ..models.financial_instrument_use_of_income_type_enum import FinancialInstrumentUseOfIncomeTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentDisplayData")


@_attrs_define
class FinancialInstrumentDisplayData:
    """
    Attributes:
        asset_type (Union[Unset, FinancialInstrumentAssetTypeEnum]):
        sub_asset_type (Union[Unset, FinancialInstrumentAssetSubtypeEnum]):
        prospectus_link (Union[Unset, str]):
        description (Union[Unset, str]):
        replication (Union[Unset, str]):
        investment_style (Union[Unset, str]):
        use_of_income (Union[Unset, FinancialInstrumentUseOfIncomeTypeEnum]):
        instrument_name (Union[Unset, str]):
        instrument_nickname (Union[Unset, str]):
        underlying_instrument_name (Union[Unset, str]):
        underlying_instrument_nickname (Union[Unset, str]):
        link_to_underlying (Union[Unset, str]):
    """

    asset_type: Union[Unset, FinancialInstrumentAssetTypeEnum] = UNSET
    sub_asset_type: Union[Unset, FinancialInstrumentAssetSubtypeEnum] = UNSET
    prospectus_link: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    replication: Union[Unset, str] = UNSET
    investment_style: Union[Unset, str] = UNSET
    use_of_income: Union[Unset, FinancialInstrumentUseOfIncomeTypeEnum] = UNSET
    instrument_name: Union[Unset, str] = UNSET
    instrument_nickname: Union[Unset, str] = UNSET
    underlying_instrument_name: Union[Unset, str] = UNSET
    underlying_instrument_nickname: Union[Unset, str] = UNSET
    link_to_underlying: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_type: Union[Unset, str] = UNSET
        if not isinstance(self.asset_type, Unset):
            asset_type = self.asset_type.value

        sub_asset_type: Union[Unset, str] = UNSET
        if not isinstance(self.sub_asset_type, Unset):
            sub_asset_type = self.sub_asset_type.value

        prospectus_link = self.prospectus_link

        description = self.description

        replication = self.replication

        investment_style = self.investment_style

        use_of_income: Union[Unset, str] = UNSET
        if not isinstance(self.use_of_income, Unset):
            use_of_income = self.use_of_income.value

        instrument_name = self.instrument_name

        instrument_nickname = self.instrument_nickname

        underlying_instrument_name = self.underlying_instrument_name

        underlying_instrument_nickname = self.underlying_instrument_nickname

        link_to_underlying = self.link_to_underlying

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asset_type is not UNSET:
            field_dict["assetType"] = asset_type
        if sub_asset_type is not UNSET:
            field_dict["subAssetType"] = sub_asset_type
        if prospectus_link is not UNSET:
            field_dict["prospectusLink"] = prospectus_link
        if description is not UNSET:
            field_dict["description"] = description
        if replication is not UNSET:
            field_dict["replication"] = replication
        if investment_style is not UNSET:
            field_dict["investmentStyle"] = investment_style
        if use_of_income is not UNSET:
            field_dict["useOfIncome"] = use_of_income
        if instrument_name is not UNSET:
            field_dict["instrumentName"] = instrument_name
        if instrument_nickname is not UNSET:
            field_dict["instrumentNickname"] = instrument_nickname
        if underlying_instrument_name is not UNSET:
            field_dict["underlyingInstrumentName"] = underlying_instrument_name
        if underlying_instrument_nickname is not UNSET:
            field_dict["underlyingInstrumentNickname"] = underlying_instrument_nickname
        if link_to_underlying is not UNSET:
            field_dict["linkToUnderlying"] = link_to_underlying

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _asset_type = d.pop("assetType", UNSET)
        asset_type: Union[Unset, FinancialInstrumentAssetTypeEnum]
        if isinstance(_asset_type, Unset):
            asset_type = UNSET
        else:
            asset_type = FinancialInstrumentAssetTypeEnum(_asset_type)

        _sub_asset_type = d.pop("subAssetType", UNSET)
        sub_asset_type: Union[Unset, FinancialInstrumentAssetSubtypeEnum]
        if isinstance(_sub_asset_type, Unset):
            sub_asset_type = UNSET
        else:
            sub_asset_type = FinancialInstrumentAssetSubtypeEnum(_sub_asset_type)

        prospectus_link = d.pop("prospectusLink", UNSET)

        description = d.pop("description", UNSET)

        replication = d.pop("replication", UNSET)

        investment_style = d.pop("investmentStyle", UNSET)

        _use_of_income = d.pop("useOfIncome", UNSET)
        use_of_income: Union[Unset, FinancialInstrumentUseOfIncomeTypeEnum]
        if isinstance(_use_of_income, Unset):
            use_of_income = UNSET
        else:
            use_of_income = FinancialInstrumentUseOfIncomeTypeEnum(_use_of_income)

        instrument_name = d.pop("instrumentName", UNSET)

        instrument_nickname = d.pop("instrumentNickname", UNSET)

        underlying_instrument_name = d.pop("underlyingInstrumentName", UNSET)

        underlying_instrument_nickname = d.pop("underlyingInstrumentNickname", UNSET)

        link_to_underlying = d.pop("linkToUnderlying", UNSET)

        financial_instrument_display_data = cls(
            asset_type=asset_type,
            sub_asset_type=sub_asset_type,
            prospectus_link=prospectus_link,
            description=description,
            replication=replication,
            investment_style=investment_style,
            use_of_income=use_of_income,
            instrument_name=instrument_name,
            instrument_nickname=instrument_nickname,
            underlying_instrument_name=underlying_instrument_name,
            underlying_instrument_nickname=underlying_instrument_nickname,
            link_to_underlying=link_to_underlying,
        )

        financial_instrument_display_data.additional_properties = d
        return financial_instrument_display_data

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
