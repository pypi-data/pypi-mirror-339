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
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.wallet_designation_enum import WalletDesignationEnum
from ..models.wallet_status_enum import WalletStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Wallet")


@_attrs_define
class Wallet:
    """
    Attributes:
        id (str):
        address (str): The blockchain address of the wallet
        owner (UUID): The ID of a legal entity or a natural person that this wallet belongs to
        creation_date (Union[Unset, datetime.datetime]):
        modification_date (Union[Unset, datetime.datetime]):
        status (Union[Unset, WalletStatusEnum]):
        description (Union[Unset, str]): Free text field to help the owner distinguish between multiple wallets
        designation (Union[Unset, WalletDesignationEnum]):
    """

    id: str
    address: str
    owner: UUID
    creation_date: Union[Unset, datetime.datetime] = UNSET
    modification_date: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, WalletStatusEnum] = UNSET
    description: Union[Unset, str] = UNSET
    designation: Union[Unset, WalletDesignationEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        address = self.address

        owner = str(self.owner)

        creation_date: Union[Unset, str] = UNSET
        if not isinstance(self.creation_date, Unset):
            creation_date = self.creation_date.isoformat()

        modification_date: Union[Unset, str] = UNSET
        if not isinstance(self.modification_date, Unset):
            modification_date = self.modification_date.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        description = self.description

        designation: Union[Unset, str] = UNSET
        if not isinstance(self.designation, Unset):
            designation = self.designation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "address": address,
                "owner": owner,
            }
        )
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if modification_date is not UNSET:
            field_dict["modificationDate"] = modification_date
        if status is not UNSET:
            field_dict["status"] = status
        if description is not UNSET:
            field_dict["description"] = description
        if designation is not UNSET:
            field_dict["designation"] = designation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        address = d.pop("address")

        owner = UUID(d.pop("owner"))

        _creation_date = d.pop("creationDate", UNSET)
        creation_date: Union[Unset, datetime.datetime]
        if isinstance(_creation_date, Unset):
            creation_date = UNSET
        else:
            creation_date = isoparse(_creation_date)

        _modification_date = d.pop("modificationDate", UNSET)
        modification_date: Union[Unset, datetime.datetime]
        if isinstance(_modification_date, Unset):
            modification_date = UNSET
        else:
            modification_date = isoparse(_modification_date)

        _status = d.pop("status", UNSET)
        status: Union[Unset, WalletStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WalletStatusEnum(_status)

        description = d.pop("description", UNSET)

        _designation = d.pop("designation", UNSET)
        designation: Union[Unset, WalletDesignationEnum]
        if isinstance(_designation, Unset):
            designation = UNSET
        else:
            designation = WalletDesignationEnum(_designation)

        wallet = cls(
            id=id,
            address=address,
            owner=owner,
            creation_date=creation_date,
            modification_date=modification_date,
            status=status,
            description=description,
            designation=designation,
        )

        wallet.additional_properties = d
        return wallet

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
