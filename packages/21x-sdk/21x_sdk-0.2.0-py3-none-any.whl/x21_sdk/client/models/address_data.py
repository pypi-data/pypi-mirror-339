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

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddressData")


@_attrs_define
class AddressData:
    """
    Attributes:
        country_code (str):
        area_code (str):
        city (str):
        street (str):
        post_office_box (Union[Unset, str]):
        address_supplement (Union[Unset, str]):
    """

    country_code: str
    area_code: str
    city: str
    street: str
    post_office_box: Union[Unset, str] = UNSET
    address_supplement: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        country_code = self.country_code

        area_code = self.area_code

        city = self.city

        street = self.street

        post_office_box = self.post_office_box

        address_supplement = self.address_supplement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "countryCode": country_code,
                "areaCode": area_code,
                "city": city,
                "street": street,
            }
        )
        if post_office_box is not UNSET:
            field_dict["postOfficeBox"] = post_office_box
        if address_supplement is not UNSET:
            field_dict["addressSupplement"] = address_supplement

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        country_code = d.pop("countryCode")

        area_code = d.pop("areaCode")

        city = d.pop("city")

        street = d.pop("street")

        post_office_box = d.pop("postOfficeBox", UNSET)

        address_supplement = d.pop("addressSupplement", UNSET)

        address_data = cls(
            country_code=country_code,
            area_code=area_code,
            city=city,
            street=street,
            post_office_box=post_office_box,
            address_supplement=address_supplement,
        )

        address_data.additional_properties = d
        return address_data

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
