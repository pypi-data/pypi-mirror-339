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
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppError")


@_attrs_define
class AppError:
    """
    Attributes:
        code (str): A identifier that categorizes the error
        message (str): A brief, human-readable message about the error
        status (Union[Unset, int]): The HTTP response code
        path (Union[Unset, str]): A URI that identifies the specific occurrence of the error
        timestamp (Union[Unset, datetime.datetime]):
        details (Union[Unset, list[str]]): Detailed explanations of the error
    """

    code: str
    message: str
    status: Union[Unset, int] = UNSET
    path: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    details: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        status = self.status

        path = self.path

        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        details: Union[Unset, list[str]] = UNSET
        if not isinstance(self.details, Unset):
            details = self.details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if path is not UNSET:
            field_dict["path"] = path
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        status = d.pop("status", UNSET)

        path = d.pop("path", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        details = cast(list[str], d.pop("details", UNSET))

        app_error = cls(
            code=code,
            message=message,
            status=status,
            path=path,
            timestamp=timestamp,
            details=details,
        )

        app_error.additional_properties = d
        return app_error

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
