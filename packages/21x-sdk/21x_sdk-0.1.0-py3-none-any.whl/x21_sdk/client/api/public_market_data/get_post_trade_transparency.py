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
from ...models.post_trade_transparency_data_list import PostTradeTransparencyDataList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    tradingpair: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
    count: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["tradingpair"] = tradingpair

    params["cursor"] = cursor

    params["limit"] = limit

    params["count"] = count

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/posttrade/recent",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[PostTradeTransparencyDataList]:
    if response.status_code == 200:
        response_200 = PostTradeTransparencyDataList.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PostTradeTransparencyDataList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tradingpair: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
    count: Union[Unset, bool] = UNSET,
) -> Response[PostTradeTransparencyDataList]:
    """getPostTradeTransparency

     Anonymous endpoint that fetches regulatory post-trade transparency data from the entire exchange,
    showing most recent trades first. If a trading pair ID is specified, the results are limited to
    trades related to that trading pair.

    Args:
        tradingpair (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):
        count (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostTradeTransparencyDataList]
    """

    kwargs = _get_kwargs(
        tradingpair=tradingpair,
        cursor=cursor,
        limit=limit,
        count=count,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    tradingpair: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
    count: Union[Unset, bool] = UNSET,
) -> Optional[PostTradeTransparencyDataList]:
    """getPostTradeTransparency

     Anonymous endpoint that fetches regulatory post-trade transparency data from the entire exchange,
    showing most recent trades first. If a trading pair ID is specified, the results are limited to
    trades related to that trading pair.

    Args:
        tradingpair (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):
        count (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostTradeTransparencyDataList
    """

    return sync_detailed(
        client=client,
        tradingpair=tradingpair,
        cursor=cursor,
        limit=limit,
        count=count,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tradingpair: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
    count: Union[Unset, bool] = UNSET,
) -> Response[PostTradeTransparencyDataList]:
    """getPostTradeTransparency

     Anonymous endpoint that fetches regulatory post-trade transparency data from the entire exchange,
    showing most recent trades first. If a trading pair ID is specified, the results are limited to
    trades related to that trading pair.

    Args:
        tradingpair (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):
        count (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PostTradeTransparencyDataList]
    """

    kwargs = _get_kwargs(
        tradingpair=tradingpair,
        cursor=cursor,
        limit=limit,
        count=count,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tradingpair: Union[Unset, str] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
    count: Union[Unset, bool] = UNSET,
) -> Optional[PostTradeTransparencyDataList]:
    """getPostTradeTransparency

     Anonymous endpoint that fetches regulatory post-trade transparency data from the entire exchange,
    showing most recent trades first. If a trading pair ID is specified, the results are limited to
    trades related to that trading pair.

    Args:
        tradingpair (Union[Unset, str]):
        cursor (Union[Unset, str]):
        limit (Union[Unset, int]):
        count (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PostTradeTransparencyDataList
    """

    return (
        await asyncio_detailed(
            client=client,
            tradingpair=tradingpair,
            cursor=cursor,
            limit=limit,
            count=count,
        )
    ).parsed
