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

from ..models.financial_instrument_linked_entity_type_enum import FinancialInstrumentLinkedEntityTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinancialInstrumentLinkedEntityData")


@_attrs_define
class FinancialInstrumentLinkedEntityData:
    """
    Attributes:
        entity_type (FinancialInstrumentLinkedEntityTypeEnum):
        entity_id (Union[Unset, str]):
        entity_name (Union[Unset, str]):
    """

    entity_type: FinancialInstrumentLinkedEntityTypeEnum
    entity_id: Union[Unset, str] = UNSET
    entity_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity_type = self.entity_type.value

        entity_id = self.entity_id

        entity_name = self.entity_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entityType": entity_type,
            }
        )
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if entity_name is not UNSET:
            field_dict["entityName"] = entity_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entity_type = FinancialInstrumentLinkedEntityTypeEnum(d.pop("entityType"))

        entity_id = d.pop("entityId", UNSET)

        entity_name = d.pop("entityName", UNSET)

        financial_instrument_linked_entity_data = cls(
            entity_type=entity_type,
            entity_id=entity_id,
            entity_name=entity_name,
        )

        financial_instrument_linked_entity_data.additional_properties = d
        return financial_instrument_linked_entity_data

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
