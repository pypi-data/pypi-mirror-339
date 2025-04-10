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
from ...models.wallet_reduced import WalletReduced
from ...types import Response


def _get_kwargs(
    wallet_address: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/wallets/byaddress/{wallet_address}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WalletReduced]:
    if response.status_code == 200:
        response_200 = WalletReduced.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WalletReduced]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    wallet_address: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[WalletReduced]:
    """getWalletByAddress

     Returns public information about a wallet specified by its address

    Args:
        wallet_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WalletReduced]
    """

    kwargs = _get_kwargs(
        wallet_address=wallet_address,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    wallet_address: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[WalletReduced]:
    """getWalletByAddress

     Returns public information about a wallet specified by its address

    Args:
        wallet_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WalletReduced
    """

    return sync_detailed(
        wallet_address=wallet_address,
        client=client,
    ).parsed


async def asyncio_detailed(
    wallet_address: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[WalletReduced]:
    """getWalletByAddress

     Returns public information about a wallet specified by its address

    Args:
        wallet_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WalletReduced]
    """

    kwargs = _get_kwargs(
        wallet_address=wallet_address,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    wallet_address: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[WalletReduced]:
    """getWalletByAddress

     Returns public information about a wallet specified by its address

    Args:
        wallet_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WalletReduced
    """

    return (
        await asyncio_detailed(
            wallet_address=wallet_address,
            client=client,
        )
    ).parsed
