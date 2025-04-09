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
    from ..models.address_data import AddressData


T = TypeVar("T", bound="PublicIssuerData")


@_attrs_define
class PublicIssuerData:
    """
    Attributes:
        company_name (Union[Unset, str]):
        website (Union[Unset, str]):
        legal_address (Union[Unset, AddressData]):
        legal_entity_identifier (Union[Unset, str]):
    """

    company_name: Union[Unset, str] = UNSET
    website: Union[Unset, str] = UNSET
    legal_address: Union[Unset, "AddressData"] = UNSET
    legal_entity_identifier: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        company_name = self.company_name

        website = self.website

        legal_address: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.legal_address, Unset):
            legal_address = self.legal_address.to_dict()

        legal_entity_identifier = self.legal_entity_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if company_name is not UNSET:
            field_dict["companyName"] = company_name
        if website is not UNSET:
            field_dict["website"] = website
        if legal_address is not UNSET:
            field_dict["legalAddress"] = legal_address
        if legal_entity_identifier is not UNSET:
            field_dict["legalEntityIdentifier"] = legal_entity_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.address_data import AddressData

        d = dict(src_dict)
        company_name = d.pop("companyName", UNSET)

        website = d.pop("website", UNSET)

        _legal_address = d.pop("legalAddress", UNSET)
        legal_address: Union[Unset, AddressData]
        if isinstance(_legal_address, Unset):
            legal_address = UNSET
        else:
            legal_address = AddressData.from_dict(_legal_address)

        legal_entity_identifier = d.pop("legalEntityIdentifier", UNSET)

        public_issuer_data = cls(
            company_name=company_name,
            website=website,
            legal_address=legal_address,
            legal_entity_identifier=legal_entity_identifier,
        )

        public_issuer_data.additional_properties = d
        return public_issuer_data

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
