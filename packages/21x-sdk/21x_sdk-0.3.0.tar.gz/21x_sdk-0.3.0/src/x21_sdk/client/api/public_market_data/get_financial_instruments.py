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

from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.financial_instrument_filter_criteria import FinancialInstrumentFilterCriteria
from ...models.financial_instrument_table_base_with_id import FinancialInstrumentTableBaseWithId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: Union[Unset, "FinancialInstrumentFilterCriteria"] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_query: Union[Unset, dict[str, Any]] = UNSET
    if not isinstance(query, Unset):
        json_query = query.to_dict()
    if not isinstance(json_query, Unset):
        params.update(json_query)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/financialinstruments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["FinancialInstrumentTableBaseWithId"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FinancialInstrumentTableBaseWithId.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["FinancialInstrumentTableBaseWithId"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, "FinancialInstrumentFilterCriteria"] = UNSET,
) -> Response[list["FinancialInstrumentTableBaseWithId"]]:
    """getFinancialInstruments

     Anonymous endpoint that lists all financial instruments available for primary market trading

    Args:
        query (Union[Unset, FinancialInstrumentFilterCriteria]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['FinancialInstrumentTableBaseWithId']]
    """

    kwargs = _get_kwargs(
        query=query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, "FinancialInstrumentFilterCriteria"] = UNSET,
) -> Optional[list["FinancialInstrumentTableBaseWithId"]]:
    """getFinancialInstruments

     Anonymous endpoint that lists all financial instruments available for primary market trading

    Args:
        query (Union[Unset, FinancialInstrumentFilterCriteria]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FinancialInstrumentTableBaseWithId']
    """

    return sync_detailed(
        client=client,
        query=query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, "FinancialInstrumentFilterCriteria"] = UNSET,
) -> Response[list["FinancialInstrumentTableBaseWithId"]]:
    """getFinancialInstruments

     Anonymous endpoint that lists all financial instruments available for primary market trading

    Args:
        query (Union[Unset, FinancialInstrumentFilterCriteria]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['FinancialInstrumentTableBaseWithId']]
    """

    kwargs = _get_kwargs(
        query=query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, "FinancialInstrumentFilterCriteria"] = UNSET,
) -> Optional[list["FinancialInstrumentTableBaseWithId"]]:
    """getFinancialInstruments

     Anonymous endpoint that lists all financial instruments available for primary market trading

    Args:
        query (Union[Unset, FinancialInstrumentFilterCriteria]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['FinancialInstrumentTableBaseWithId']
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
        )
    ).parsed
