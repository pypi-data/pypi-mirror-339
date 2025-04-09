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
from ...models.order_book_result import OrderBookResult
from ...models.order_kind_enum import OrderKindEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    kind: Union[Unset, OrderKindEnum] = UNSET,
    max_: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_kind: Union[Unset, str] = UNSET
    if not isinstance(kind, Unset):
        json_kind = kind.value

    params["kind"] = json_kind

    params["max"] = max_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/tradingpairs/{id}/orderbook",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[OrderBookResult]:
    if response.status_code == 200:
        response_200 = OrderBookResult.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OrderBookResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, OrderKindEnum] = UNSET,
    max_: Union[Unset, int] = UNSET,
) -> Response[OrderBookResult]:
    """getOrderBookTopOrders

     Anonymous endpoint that fetches the first x open orders in the order book

    Args:
        id (str):
        kind (Union[Unset, OrderKindEnum]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderBookResult]
    """

    kwargs = _get_kwargs(
        id=id,
        kind=kind,
        max_=max_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, OrderKindEnum] = UNSET,
    max_: Union[Unset, int] = UNSET,
) -> Optional[OrderBookResult]:
    """getOrderBookTopOrders

     Anonymous endpoint that fetches the first x open orders in the order book

    Args:
        id (str):
        kind (Union[Unset, OrderKindEnum]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderBookResult
    """

    return sync_detailed(
        id=id,
        client=client,
        kind=kind,
        max_=max_,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, OrderKindEnum] = UNSET,
    max_: Union[Unset, int] = UNSET,
) -> Response[OrderBookResult]:
    """getOrderBookTopOrders

     Anonymous endpoint that fetches the first x open orders in the order book

    Args:
        id (str):
        kind (Union[Unset, OrderKindEnum]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OrderBookResult]
    """

    kwargs = _get_kwargs(
        id=id,
        kind=kind,
        max_=max_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    kind: Union[Unset, OrderKindEnum] = UNSET,
    max_: Union[Unset, int] = UNSET,
) -> Optional[OrderBookResult]:
    """getOrderBookTopOrders

     Anonymous endpoint that fetches the first x open orders in the order book

    Args:
        id (str):
        kind (Union[Unset, OrderKindEnum]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OrderBookResult
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            kind=kind,
            max_=max_,
        )
    ).parsed
