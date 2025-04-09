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

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.asset_class_of_underlying_enum import AssetClassOfUnderlyingEnum
from ..models.block_chain_enum import BlockChainEnum
from ..models.financial_instrument_contract_type_enum import FinancialInstrumentContractTypeEnum
from ..models.financial_instrument_status_enum import FinancialInstrumentStatusEnum
from ..models.mifir_identifier_enum import MifirIdentifierEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.financial_instrument_availability_data import FinancialInstrumentAvailabilityData
    from ..models.financial_instrument_commodity_derivative_data import FinancialInstrumentCommodityDerivativeData
    from ..models.financial_instrument_contracts_for_difference_data import (
        FinancialInstrumentContractsForDifferenceData,
    )
    from ..models.financial_instrument_credit_derivative_data import FinancialInstrumentCreditDerivativeData
    from ..models.financial_instrument_debt_instrument_data import FinancialInstrumentDebtInstrumentData
    from ..models.financial_instrument_derivative_data import FinancialInstrumentDerivativeData
    from ..models.financial_instrument_display_data import FinancialInstrumentDisplayData
    from ..models.financial_instrument_emission_allowance_data import FinancialInstrumentEmissionAllowanceData
    from ..models.financial_instrument_foreign_exchange_derivative_data import (
        FinancialInstrumentForeignExchangeDerivativeData,
    )
    from ..models.financial_instrument_interest_rate_derivative_data import (
        FinancialInstrumentInterestRateDerivativeData,
    )
    from ..models.financial_instrument_linked_entity_data import FinancialInstrumentLinkedEntityData
    from ..models.financial_instrument_performance_data import FinancialInstrumentPerformanceData
    from ..models.public_issuer_data import PublicIssuerData


T = TypeVar("T", bound="FinancialInstrumentPublic")


@_attrs_define
class FinancialInstrumentPublic:
    """
    Attributes:
        full_name (str):
        status (Union[Unset, FinancialInstrumentStatusEnum]):
        domicile (Union[Unset, str]):
        wkn (Union[Unset, str]):
        sedol (Union[Unset, str]):
        cusip (Union[Unset, str]):
        valor (Union[Unset, str]):
        dti (Union[Unset, str]):
        symbol (Union[Unset, str]):
        protocol (Union[Unset, BlockChainEnum]):
        smart_contract_address (Union[Unset, str]):
        isin (Union[Unset, str]):
        cfi (Union[Unset, str]):
        commodities_derivative_indicator (Union[Unset, bool]):  Default: False.
        issuer_id (Union[Unset, str]):
        issuer_name (Union[Unset, str]):
        trading_venue (Union[Unset, str]):  Default: '21XX'.
        fisn (Union[Unset, str]):
        issuer_request_for_admission_to_trade (Union[Unset, bool]):  Default: False.
        listing_date (Union[Unset, datetime.date]):
        issuer_approval_date (Union[Unset, datetime.datetime]):
        admission_to_trade_request_date (Union[Unset, datetime.datetime]):
        effective_date (Union[Unset, datetime.datetime]):
        termination_date (Union[Unset, datetime.datetime]):
        notional_currency_1 (Union[Unset, str]):  Default: 'EUR'.
        mifir_identifier (Union[Unset, MifirIdentifierEnum]):
        number_of_outstanding_instruments (Union[Unset, str]):
        holdings_exceeding_total_voting_right_threshold (Union[Unset, str]):
        issuance_size (Union[Unset, str]):
        asset_class_of_underlying (Union[Unset, AssetClassOfUnderlyingEnum]):
        maturity_date (Union[Unset, datetime.date]):
        contract_type (Union[Unset, FinancialInstrumentContractTypeEnum]):
        linked_entities (Union[Unset, list['FinancialInstrumentLinkedEntityData']]):
        availability (Union[Unset, FinancialInstrumentAvailabilityData]):
        display_data (Union[Unset, FinancialInstrumentDisplayData]):
        performance_data (Union[Unset, FinancialInstrumentPerformanceData]):
        debt_instrument_data (Union[Unset, FinancialInstrumentDebtInstrumentData]):
        derivative_data (Union[Unset, FinancialInstrumentDerivativeData]):
        commodity_derivative_data (Union[Unset, FinancialInstrumentCommodityDerivativeData]):
        interest_rate_derivative_data (Union[Unset, FinancialInstrumentInterestRateDerivativeData]):
        foreign_exchange_derivative_data (Union[Unset, FinancialInstrumentForeignExchangeDerivativeData]):
        emission_allowance_data (Union[Unset, FinancialInstrumentEmissionAllowanceData]):
        contracts_for_difference_data (Union[Unset, FinancialInstrumentContractsForDifferenceData]):
        credit_derivative_data (Union[Unset, FinancialInstrumentCreditDerivativeData]):
        internal_id (Union[Unset, str]):
        issuer_data (Union[Unset, PublicIssuerData]):
    """

    full_name: str
    status: Union[Unset, FinancialInstrumentStatusEnum] = UNSET
    domicile: Union[Unset, str] = UNSET
    wkn: Union[Unset, str] = UNSET
    sedol: Union[Unset, str] = UNSET
    cusip: Union[Unset, str] = UNSET
    valor: Union[Unset, str] = UNSET
    dti: Union[Unset, str] = UNSET
    symbol: Union[Unset, str] = UNSET
    protocol: Union[Unset, BlockChainEnum] = UNSET
    smart_contract_address: Union[Unset, str] = UNSET
    isin: Union[Unset, str] = UNSET
    cfi: Union[Unset, str] = UNSET
    commodities_derivative_indicator: Union[Unset, bool] = False
    issuer_id: Union[Unset, str] = UNSET
    issuer_name: Union[Unset, str] = UNSET
    trading_venue: Union[Unset, str] = "21XX"
    fisn: Union[Unset, str] = UNSET
    issuer_request_for_admission_to_trade: Union[Unset, bool] = False
    listing_date: Union[Unset, datetime.date] = UNSET
    issuer_approval_date: Union[Unset, datetime.datetime] = UNSET
    admission_to_trade_request_date: Union[Unset, datetime.datetime] = UNSET
    effective_date: Union[Unset, datetime.datetime] = UNSET
    termination_date: Union[Unset, datetime.datetime] = UNSET
    notional_currency_1: Union[Unset, str] = "EUR"
    mifir_identifier: Union[Unset, MifirIdentifierEnum] = UNSET
    number_of_outstanding_instruments: Union[Unset, str] = UNSET
    holdings_exceeding_total_voting_right_threshold: Union[Unset, str] = UNSET
    issuance_size: Union[Unset, str] = UNSET
    asset_class_of_underlying: Union[Unset, AssetClassOfUnderlyingEnum] = UNSET
    maturity_date: Union[Unset, datetime.date] = UNSET
    contract_type: Union[Unset, FinancialInstrumentContractTypeEnum] = UNSET
    linked_entities: Union[Unset, list["FinancialInstrumentLinkedEntityData"]] = UNSET
    availability: Union[Unset, "FinancialInstrumentAvailabilityData"] = UNSET
    display_data: Union[Unset, "FinancialInstrumentDisplayData"] = UNSET
    performance_data: Union[Unset, "FinancialInstrumentPerformanceData"] = UNSET
    debt_instrument_data: Union[Unset, "FinancialInstrumentDebtInstrumentData"] = UNSET
    derivative_data: Union[Unset, "FinancialInstrumentDerivativeData"] = UNSET
    commodity_derivative_data: Union[Unset, "FinancialInstrumentCommodityDerivativeData"] = UNSET
    interest_rate_derivative_data: Union[Unset, "FinancialInstrumentInterestRateDerivativeData"] = UNSET
    foreign_exchange_derivative_data: Union[Unset, "FinancialInstrumentForeignExchangeDerivativeData"] = UNSET
    emission_allowance_data: Union[Unset, "FinancialInstrumentEmissionAllowanceData"] = UNSET
    contracts_for_difference_data: Union[Unset, "FinancialInstrumentContractsForDifferenceData"] = UNSET
    credit_derivative_data: Union[Unset, "FinancialInstrumentCreditDerivativeData"] = UNSET
    internal_id: Union[Unset, str] = UNSET
    issuer_data: Union[Unset, "PublicIssuerData"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        domicile = self.domicile

        wkn = self.wkn

        sedol = self.sedol

        cusip = self.cusip

        valor = self.valor

        dti = self.dti

        symbol = self.symbol

        protocol: Union[Unset, str] = UNSET
        if not isinstance(self.protocol, Unset):
            protocol = self.protocol.value

        smart_contract_address = self.smart_contract_address

        isin = self.isin

        cfi = self.cfi

        commodities_derivative_indicator = self.commodities_derivative_indicator

        issuer_id = self.issuer_id

        issuer_name = self.issuer_name

        trading_venue = self.trading_venue

        fisn = self.fisn

        issuer_request_for_admission_to_trade = self.issuer_request_for_admission_to_trade

        listing_date: Union[Unset, str] = UNSET
        if not isinstance(self.listing_date, Unset):
            listing_date = self.listing_date.isoformat()

        issuer_approval_date: Union[Unset, str] = UNSET
        if not isinstance(self.issuer_approval_date, Unset):
            issuer_approval_date = self.issuer_approval_date.isoformat()

        admission_to_trade_request_date: Union[Unset, str] = UNSET
        if not isinstance(self.admission_to_trade_request_date, Unset):
            admission_to_trade_request_date = self.admission_to_trade_request_date.isoformat()

        effective_date: Union[Unset, str] = UNSET
        if not isinstance(self.effective_date, Unset):
            effective_date = self.effective_date.isoformat()

        termination_date: Union[Unset, str] = UNSET
        if not isinstance(self.termination_date, Unset):
            termination_date = self.termination_date.isoformat()

        notional_currency_1 = self.notional_currency_1

        mifir_identifier: Union[Unset, str] = UNSET
        if not isinstance(self.mifir_identifier, Unset):
            mifir_identifier = self.mifir_identifier.value

        number_of_outstanding_instruments = self.number_of_outstanding_instruments

        holdings_exceeding_total_voting_right_threshold = self.holdings_exceeding_total_voting_right_threshold

        issuance_size = self.issuance_size

        asset_class_of_underlying: Union[Unset, str] = UNSET
        if not isinstance(self.asset_class_of_underlying, Unset):
            asset_class_of_underlying = self.asset_class_of_underlying.value

        maturity_date: Union[Unset, str] = UNSET
        if not isinstance(self.maturity_date, Unset):
            maturity_date = self.maturity_date.isoformat()

        contract_type: Union[Unset, str] = UNSET
        if not isinstance(self.contract_type, Unset):
            contract_type = self.contract_type.value

        linked_entities: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.linked_entities, Unset):
            linked_entities = []
            for linked_entities_item_data in self.linked_entities:
                linked_entities_item = linked_entities_item_data.to_dict()
                linked_entities.append(linked_entities_item)

        availability: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.availability, Unset):
            availability = self.availability.to_dict()

        display_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.display_data, Unset):
            display_data = self.display_data.to_dict()

        performance_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.performance_data, Unset):
            performance_data = self.performance_data.to_dict()

        debt_instrument_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.debt_instrument_data, Unset):
            debt_instrument_data = self.debt_instrument_data.to_dict()

        derivative_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.derivative_data, Unset):
            derivative_data = self.derivative_data.to_dict()

        commodity_derivative_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.commodity_derivative_data, Unset):
            commodity_derivative_data = self.commodity_derivative_data.to_dict()

        interest_rate_derivative_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interest_rate_derivative_data, Unset):
            interest_rate_derivative_data = self.interest_rate_derivative_data.to_dict()

        foreign_exchange_derivative_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.foreign_exchange_derivative_data, Unset):
            foreign_exchange_derivative_data = self.foreign_exchange_derivative_data.to_dict()

        emission_allowance_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.emission_allowance_data, Unset):
            emission_allowance_data = self.emission_allowance_data.to_dict()

        contracts_for_difference_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.contracts_for_difference_data, Unset):
            contracts_for_difference_data = self.contracts_for_difference_data.to_dict()

        credit_derivative_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.credit_derivative_data, Unset):
            credit_derivative_data = self.credit_derivative_data.to_dict()

        internal_id = self.internal_id

        issuer_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuer_data, Unset):
            issuer_data = self.issuer_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fullName": full_name,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if domicile is not UNSET:
            field_dict["domicile"] = domicile
        if wkn is not UNSET:
            field_dict["wkn"] = wkn
        if sedol is not UNSET:
            field_dict["sedol"] = sedol
        if cusip is not UNSET:
            field_dict["cusip"] = cusip
        if valor is not UNSET:
            field_dict["valor"] = valor
        if dti is not UNSET:
            field_dict["dti"] = dti
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
        if smart_contract_address is not UNSET:
            field_dict["smartContractAddress"] = smart_contract_address
        if isin is not UNSET:
            field_dict["isin"] = isin
        if cfi is not UNSET:
            field_dict["cfi"] = cfi
        if commodities_derivative_indicator is not UNSET:
            field_dict["commoditiesDerivativeIndicator"] = commodities_derivative_indicator
        if issuer_id is not UNSET:
            field_dict["issuerId"] = issuer_id
        if issuer_name is not UNSET:
            field_dict["issuerName"] = issuer_name
        if trading_venue is not UNSET:
            field_dict["tradingVenue"] = trading_venue
        if fisn is not UNSET:
            field_dict["fisn"] = fisn
        if issuer_request_for_admission_to_trade is not UNSET:
            field_dict["issuerRequestForAdmissionToTrade"] = issuer_request_for_admission_to_trade
        if listing_date is not UNSET:
            field_dict["listingDate"] = listing_date
        if issuer_approval_date is not UNSET:
            field_dict["issuerApprovalDate"] = issuer_approval_date
        if admission_to_trade_request_date is not UNSET:
            field_dict["admissionToTradeRequestDate"] = admission_to_trade_request_date
        if effective_date is not UNSET:
            field_dict["effectiveDate"] = effective_date
        if termination_date is not UNSET:
            field_dict["terminationDate"] = termination_date
        if notional_currency_1 is not UNSET:
            field_dict["notionalCurrency1"] = notional_currency_1
        if mifir_identifier is not UNSET:
            field_dict["mifirIdentifier"] = mifir_identifier
        if number_of_outstanding_instruments is not UNSET:
            field_dict["numberOfOutstandingInstruments"] = number_of_outstanding_instruments
        if holdings_exceeding_total_voting_right_threshold is not UNSET:
            field_dict["holdingsExceedingTotalVotingRightThreshold"] = holdings_exceeding_total_voting_right_threshold
        if issuance_size is not UNSET:
            field_dict["issuanceSize"] = issuance_size
        if asset_class_of_underlying is not UNSET:
            field_dict["assetClassOfUnderlying"] = asset_class_of_underlying
        if maturity_date is not UNSET:
            field_dict["maturityDate"] = maturity_date
        if contract_type is not UNSET:
            field_dict["contractType"] = contract_type
        if linked_entities is not UNSET:
            field_dict["linkedEntities"] = linked_entities
        if availability is not UNSET:
            field_dict["availability"] = availability
        if display_data is not UNSET:
            field_dict["displayData"] = display_data
        if performance_data is not UNSET:
            field_dict["performanceData"] = performance_data
        if debt_instrument_data is not UNSET:
            field_dict["debtInstrumentData"] = debt_instrument_data
        if derivative_data is not UNSET:
            field_dict["derivativeData"] = derivative_data
        if commodity_derivative_data is not UNSET:
            field_dict["commodityDerivativeData"] = commodity_derivative_data
        if interest_rate_derivative_data is not UNSET:
            field_dict["interestRateDerivativeData"] = interest_rate_derivative_data
        if foreign_exchange_derivative_data is not UNSET:
            field_dict["foreignExchangeDerivativeData"] = foreign_exchange_derivative_data
        if emission_allowance_data is not UNSET:
            field_dict["emissionAllowanceData"] = emission_allowance_data
        if contracts_for_difference_data is not UNSET:
            field_dict["contractsForDifferenceData"] = contracts_for_difference_data
        if credit_derivative_data is not UNSET:
            field_dict["creditDerivativeData"] = credit_derivative_data
        if internal_id is not UNSET:
            field_dict["internalId"] = internal_id
        if issuer_data is not UNSET:
            field_dict["issuerData"] = issuer_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.financial_instrument_availability_data import FinancialInstrumentAvailabilityData
        from ..models.financial_instrument_commodity_derivative_data import FinancialInstrumentCommodityDerivativeData
        from ..models.financial_instrument_contracts_for_difference_data import (
            FinancialInstrumentContractsForDifferenceData,
        )
        from ..models.financial_instrument_credit_derivative_data import FinancialInstrumentCreditDerivativeData
        from ..models.financial_instrument_debt_instrument_data import FinancialInstrumentDebtInstrumentData
        from ..models.financial_instrument_derivative_data import FinancialInstrumentDerivativeData
        from ..models.financial_instrument_display_data import FinancialInstrumentDisplayData
        from ..models.financial_instrument_emission_allowance_data import FinancialInstrumentEmissionAllowanceData
        from ..models.financial_instrument_foreign_exchange_derivative_data import (
            FinancialInstrumentForeignExchangeDerivativeData,
        )
        from ..models.financial_instrument_interest_rate_derivative_data import (
            FinancialInstrumentInterestRateDerivativeData,
        )
        from ..models.financial_instrument_linked_entity_data import FinancialInstrumentLinkedEntityData
        from ..models.financial_instrument_performance_data import FinancialInstrumentPerformanceData
        from ..models.public_issuer_data import PublicIssuerData

        d = dict(src_dict)
        full_name = d.pop("fullName")

        _status = d.pop("status", UNSET)
        status: Union[Unset, FinancialInstrumentStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = FinancialInstrumentStatusEnum(_status)

        domicile = d.pop("domicile", UNSET)

        wkn = d.pop("wkn", UNSET)

        sedol = d.pop("sedol", UNSET)

        cusip = d.pop("cusip", UNSET)

        valor = d.pop("valor", UNSET)

        dti = d.pop("dti", UNSET)

        symbol = d.pop("symbol", UNSET)

        _protocol = d.pop("protocol", UNSET)
        protocol: Union[Unset, BlockChainEnum]
        if isinstance(_protocol, Unset):
            protocol = UNSET
        else:
            protocol = BlockChainEnum(_protocol)

        smart_contract_address = d.pop("smartContractAddress", UNSET)

        isin = d.pop("isin", UNSET)

        cfi = d.pop("cfi", UNSET)

        commodities_derivative_indicator = d.pop("commoditiesDerivativeIndicator", UNSET)

        issuer_id = d.pop("issuerId", UNSET)

        issuer_name = d.pop("issuerName", UNSET)

        trading_venue = d.pop("tradingVenue", UNSET)

        fisn = d.pop("fisn", UNSET)

        issuer_request_for_admission_to_trade = d.pop("issuerRequestForAdmissionToTrade", UNSET)

        _listing_date = d.pop("listingDate", UNSET)
        listing_date: Union[Unset, datetime.date]
        if isinstance(_listing_date, Unset):
            listing_date = UNSET
        else:
            listing_date = isoparse(_listing_date).date()

        _issuer_approval_date = d.pop("issuerApprovalDate", UNSET)
        issuer_approval_date: Union[Unset, datetime.datetime]
        if isinstance(_issuer_approval_date, Unset):
            issuer_approval_date = UNSET
        else:
            issuer_approval_date = isoparse(_issuer_approval_date)

        _admission_to_trade_request_date = d.pop("admissionToTradeRequestDate", UNSET)
        admission_to_trade_request_date: Union[Unset, datetime.datetime]
        if isinstance(_admission_to_trade_request_date, Unset):
            admission_to_trade_request_date = UNSET
        else:
            admission_to_trade_request_date = isoparse(_admission_to_trade_request_date)

        _effective_date = d.pop("effectiveDate", UNSET)
        effective_date: Union[Unset, datetime.datetime]
        if isinstance(_effective_date, Unset):
            effective_date = UNSET
        else:
            effective_date = isoparse(_effective_date)

        _termination_date = d.pop("terminationDate", UNSET)
        termination_date: Union[Unset, datetime.datetime]
        if isinstance(_termination_date, Unset):
            termination_date = UNSET
        else:
            termination_date = isoparse(_termination_date)

        notional_currency_1 = d.pop("notionalCurrency1", UNSET)

        _mifir_identifier = d.pop("mifirIdentifier", UNSET)
        mifir_identifier: Union[Unset, MifirIdentifierEnum]
        if isinstance(_mifir_identifier, Unset):
            mifir_identifier = UNSET
        else:
            mifir_identifier = MifirIdentifierEnum(_mifir_identifier)

        number_of_outstanding_instruments = d.pop("numberOfOutstandingInstruments", UNSET)

        holdings_exceeding_total_voting_right_threshold = d.pop("holdingsExceedingTotalVotingRightThreshold", UNSET)

        issuance_size = d.pop("issuanceSize", UNSET)

        _asset_class_of_underlying = d.pop("assetClassOfUnderlying", UNSET)
        asset_class_of_underlying: Union[Unset, AssetClassOfUnderlyingEnum]
        if isinstance(_asset_class_of_underlying, Unset):
            asset_class_of_underlying = UNSET
        else:
            asset_class_of_underlying = AssetClassOfUnderlyingEnum(_asset_class_of_underlying)

        _maturity_date = d.pop("maturityDate", UNSET)
        maturity_date: Union[Unset, datetime.date]
        if isinstance(_maturity_date, Unset):
            maturity_date = UNSET
        else:
            maturity_date = isoparse(_maturity_date).date()

        _contract_type = d.pop("contractType", UNSET)
        contract_type: Union[Unset, FinancialInstrumentContractTypeEnum]
        if isinstance(_contract_type, Unset):
            contract_type = UNSET
        else:
            contract_type = FinancialInstrumentContractTypeEnum(_contract_type)

        linked_entities = []
        _linked_entities = d.pop("linkedEntities", UNSET)
        for linked_entities_item_data in _linked_entities or []:
            linked_entities_item = FinancialInstrumentLinkedEntityData.from_dict(linked_entities_item_data)

            linked_entities.append(linked_entities_item)

        _availability = d.pop("availability", UNSET)
        availability: Union[Unset, FinancialInstrumentAvailabilityData]
        if isinstance(_availability, Unset):
            availability = UNSET
        else:
            availability = FinancialInstrumentAvailabilityData.from_dict(_availability)

        _display_data = d.pop("displayData", UNSET)
        display_data: Union[Unset, FinancialInstrumentDisplayData]
        if isinstance(_display_data, Unset):
            display_data = UNSET
        else:
            display_data = FinancialInstrumentDisplayData.from_dict(_display_data)

        _performance_data = d.pop("performanceData", UNSET)
        performance_data: Union[Unset, FinancialInstrumentPerformanceData]
        if isinstance(_performance_data, Unset):
            performance_data = UNSET
        else:
            performance_data = FinancialInstrumentPerformanceData.from_dict(_performance_data)

        _debt_instrument_data = d.pop("debtInstrumentData", UNSET)
        debt_instrument_data: Union[Unset, FinancialInstrumentDebtInstrumentData]
        if isinstance(_debt_instrument_data, Unset):
            debt_instrument_data = UNSET
        else:
            debt_instrument_data = FinancialInstrumentDebtInstrumentData.from_dict(_debt_instrument_data)

        _derivative_data = d.pop("derivativeData", UNSET)
        derivative_data: Union[Unset, FinancialInstrumentDerivativeData]
        if isinstance(_derivative_data, Unset):
            derivative_data = UNSET
        else:
            derivative_data = FinancialInstrumentDerivativeData.from_dict(_derivative_data)

        _commodity_derivative_data = d.pop("commodityDerivativeData", UNSET)
        commodity_derivative_data: Union[Unset, FinancialInstrumentCommodityDerivativeData]
        if isinstance(_commodity_derivative_data, Unset):
            commodity_derivative_data = UNSET
        else:
            commodity_derivative_data = FinancialInstrumentCommodityDerivativeData.from_dict(_commodity_derivative_data)

        _interest_rate_derivative_data = d.pop("interestRateDerivativeData", UNSET)
        interest_rate_derivative_data: Union[Unset, FinancialInstrumentInterestRateDerivativeData]
        if isinstance(_interest_rate_derivative_data, Unset):
            interest_rate_derivative_data = UNSET
        else:
            interest_rate_derivative_data = FinancialInstrumentInterestRateDerivativeData.from_dict(
                _interest_rate_derivative_data
            )

        _foreign_exchange_derivative_data = d.pop("foreignExchangeDerivativeData", UNSET)
        foreign_exchange_derivative_data: Union[Unset, FinancialInstrumentForeignExchangeDerivativeData]
        if isinstance(_foreign_exchange_derivative_data, Unset):
            foreign_exchange_derivative_data = UNSET
        else:
            foreign_exchange_derivative_data = FinancialInstrumentForeignExchangeDerivativeData.from_dict(
                _foreign_exchange_derivative_data
            )

        _emission_allowance_data = d.pop("emissionAllowanceData", UNSET)
        emission_allowance_data: Union[Unset, FinancialInstrumentEmissionAllowanceData]
        if isinstance(_emission_allowance_data, Unset):
            emission_allowance_data = UNSET
        else:
            emission_allowance_data = FinancialInstrumentEmissionAllowanceData.from_dict(_emission_allowance_data)

        _contracts_for_difference_data = d.pop("contractsForDifferenceData", UNSET)
        contracts_for_difference_data: Union[Unset, FinancialInstrumentContractsForDifferenceData]
        if isinstance(_contracts_for_difference_data, Unset):
            contracts_for_difference_data = UNSET
        else:
            contracts_for_difference_data = FinancialInstrumentContractsForDifferenceData.from_dict(
                _contracts_for_difference_data
            )

        _credit_derivative_data = d.pop("creditDerivativeData", UNSET)
        credit_derivative_data: Union[Unset, FinancialInstrumentCreditDerivativeData]
        if isinstance(_credit_derivative_data, Unset):
            credit_derivative_data = UNSET
        else:
            credit_derivative_data = FinancialInstrumentCreditDerivativeData.from_dict(_credit_derivative_data)

        internal_id = d.pop("internalId", UNSET)

        _issuer_data = d.pop("issuerData", UNSET)
        issuer_data: Union[Unset, PublicIssuerData]
        if isinstance(_issuer_data, Unset):
            issuer_data = UNSET
        else:
            issuer_data = PublicIssuerData.from_dict(_issuer_data)

        financial_instrument_public = cls(
            full_name=full_name,
            status=status,
            domicile=domicile,
            wkn=wkn,
            sedol=sedol,
            cusip=cusip,
            valor=valor,
            dti=dti,
            symbol=symbol,
            protocol=protocol,
            smart_contract_address=smart_contract_address,
            isin=isin,
            cfi=cfi,
            commodities_derivative_indicator=commodities_derivative_indicator,
            issuer_id=issuer_id,
            issuer_name=issuer_name,
            trading_venue=trading_venue,
            fisn=fisn,
            issuer_request_for_admission_to_trade=issuer_request_for_admission_to_trade,
            listing_date=listing_date,
            issuer_approval_date=issuer_approval_date,
            admission_to_trade_request_date=admission_to_trade_request_date,
            effective_date=effective_date,
            termination_date=termination_date,
            notional_currency_1=notional_currency_1,
            mifir_identifier=mifir_identifier,
            number_of_outstanding_instruments=number_of_outstanding_instruments,
            holdings_exceeding_total_voting_right_threshold=holdings_exceeding_total_voting_right_threshold,
            issuance_size=issuance_size,
            asset_class_of_underlying=asset_class_of_underlying,
            maturity_date=maturity_date,
            contract_type=contract_type,
            linked_entities=linked_entities,
            availability=availability,
            display_data=display_data,
            performance_data=performance_data,
            debt_instrument_data=debt_instrument_data,
            derivative_data=derivative_data,
            commodity_derivative_data=commodity_derivative_data,
            interest_rate_derivative_data=interest_rate_derivative_data,
            foreign_exchange_derivative_data=foreign_exchange_derivative_data,
            emission_allowance_data=emission_allowance_data,
            contracts_for_difference_data=contracts_for_difference_data,
            credit_derivative_data=credit_derivative_data,
            internal_id=internal_id,
            issuer_data=issuer_data,
        )

        financial_instrument_public.additional_properties = d
        return financial_instrument_public

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
