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

import os

import httpx
from attrs import define, field
from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client
from authlib.oauth2.rfc6749 import OAuth2Token

from x21_sdk import client as base_client


@define
class Client(base_client.Client):

    _base_url: str = field(default=os.environ.get("21X_BASE_URL"), alias="base_url")
    raise_on_unexpected_status: bool = field(default=True, kw_only=True)


@define
class AuthenticatedClient(base_client.Client):

    _base_url: str = field(default=os.environ.get("21X_BASE_URL"), alias="base_url")
    _client_id: str = field(default=os.environ.get("21X_AUTH_CLIENT_ID"), alias="client_id")
    _client_secret: str = field(default=os.environ.get("21X_AUTH_CLIENT_SECRET"), alias="client_secret")
    _token_endpoint: str = field(default=os.environ.get("21X_AUTH_CLIENT_TOKEN_ENDPOINT"), alias="token_endpoint")

    raise_on_unexpected_status: bool = field(default=True, kw_only=True)

    # oauth2 addon
    _raw_token: OAuth2Token = field(default=None, init=False)

    _oauth_client: OAuth2Client = field(default=None, init=False)
    _async_oauth_client: AsyncOAuth2Client = field(default=None, init=False)

    def fetch_token(self) -> OAuth2Token:
        if self._oauth_client is None:
            self.get_httpx_client()

        self._raw_token = self._oauth_client.fetch_token(url=self._token_endpoint)
        return self._raw_token

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = self._oauth_client = OAuth2Client(
                self._client_id,
                self._client_secret,
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )

        return self._client

    async def async_fetch_token(self) -> OAuth2Token:
        if self._async_oauth_client is None:
            self.get_async_httpx_client()

        self._raw_token = await self._async_oauth_client.fetch_token(url=self._token_endpoint)
        return self._raw_token

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = self._async_oauth_client = AsyncOAuth2Client(
                self._client_id,
                self._client_secret,
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )

        return self._async_client
