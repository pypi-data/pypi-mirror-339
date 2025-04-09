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

from ..models.wallet_designation_enum import WalletDesignationEnum
from ..models.wallet_status_enum import WalletStatusEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="WalletReduced")


@_attrs_define
class WalletReduced:
    """
    Attributes:
        address (Union[Unset, str]): The blockchain address of the wallet
        status (Union[Unset, WalletStatusEnum]):
        designation (Union[Unset, WalletDesignationEnum]):
    """

    address: Union[Unset, str] = UNSET
    status: Union[Unset, WalletStatusEnum] = UNSET
    designation: Union[Unset, WalletDesignationEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        address = self.address

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        designation: Union[Unset, str] = UNSET
        if not isinstance(self.designation, Unset):
            designation = self.designation.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if address is not UNSET:
            field_dict["address"] = address
        if status is not UNSET:
            field_dict["status"] = status
        if designation is not UNSET:
            field_dict["designation"] = designation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        address = d.pop("address", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, WalletStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = WalletStatusEnum(_status)

        _designation = d.pop("designation", UNSET)
        designation: Union[Unset, WalletDesignationEnum]
        if isinstance(_designation, Unset):
            designation = UNSET
        else:
            designation = WalletDesignationEnum(_designation)

        wallet_reduced = cls(
            address=address,
            status=status,
            designation=designation,
        )

        wallet_reduced.additional_properties = d
        return wallet_reduced

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
