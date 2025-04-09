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

from decimal import Decimal

import eth_abi
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware, SignAndSendRawMiddlewareBuilder
from web3.types import TxParams

from onchain import logger, util
from onchain.abi import orderbook_abi, token_abi, whitelist_abi
from onchain.types import (
    ClientInfo,
    OrderBookOrders,
    OrderBookOrderCount,
    OrderBookPhase,
    Pair,
    PairConfiguration,
    PreTradeControlConfig,
    VolatilityManagementConfig,
)


class OrderBook:
    """EDX Trading Pair

    Handler for Order Book interaction for creating buy and sell orders.
    """

    def __init__(
        self,
        account: str,
        orderbook_addr: str,
        provider_url: str,
        admin_wallet: str = None,
    ):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))

        eth = self.w3.eth

        # add account as auto-signer
        self.account = eth.account.from_key(account)
        self.wallet = self.account.address
        self.admin = eth.account.from_key(admin_wallet) if admin_wallet else None

        signers = [self.account, self.admin] if self.admin else [self.account]

        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        self.w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(signers), layer=0)

        self.contract = eth.contract(orderbook_addr, abi=orderbook_abi)

        # assign relevant contract addresses and fetch trading pair addresses
        self.orderbook_addr = orderbook_addr

        self.config = self._fetch_pair_configuration()

        self.base_contract = eth.contract(self.config.base_token_address, abi=token_abi)
        self.quote_contract = eth.contract(self.config.quote_token_address, abi=token_abi)
        self.whitelist_contract = eth.contract(self.config.whitelist_address, abi=whitelist_abi)

        self.name = self._fetch_pair_symbols()

        self.log = logger.getLogger(f"pair: {self.name} wallet: {self.wallet}")

        self.nonce = self.w3.eth.get_transaction_count(self.wallet)

    def _handle_transaction(self, transaction: TxParams):
        """Process a transaction to completion"""

        if transaction["maxPriorityFeePerGas"] > transaction["maxFeePerGas"]:
            transaction["maxFeePerGas"] = transaction["maxPriorityFeePerGas"] + 1

        tx_hash = self.w3.eth.send_transaction(transaction)

        self.log.info("https://www.oklink.com/amoy/tx/%s", tx_hash.hex())

        self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300, poll_latency=0.5)

    def _fetch_pair_symbols(self):
        base_symbol = self.base_contract.functions.symbol().call()
        quote_symbol = self.quote_contract.functions.symbol().call()

        return f"{base_symbol}/{quote_symbol}"

    def _fetch_pair_configuration(self) -> PairConfiguration:
        """Fetch the trading pair configuration from the Order Book contract"""
        response = self.contract.functions.getConfig().call()

        return PairConfiguration(
            base_scale=Decimal(response[0][0][0]),
            quote_scale=Decimal(response[0][1][0]),
            base_native_scale=Decimal(response[0][0][1]),
            quote_native_scale=Decimal(response[0][1][1]),
            maker_commission=response[1],
            taker_commission=response[2],
            market_maker_commission=response[3],
            quote_token_address=response[4],
            base_token_address=response[5],
            whitelist_address=response[6],
            commission_wallet=response[7],
            base_token_fallback_wallet=response[8],
            quote_token_fallback_wallet=response[9],
            liquidity_band=response[10],
            version=util.convert_bytes_version_to_string(response[11]),
        )

    def _get_order_book_phase(self) -> OrderBookPhase:
        """Get the order book phase from the Order Book contract"""
        response = self.contract.functions.getOrderBookPhase().call()

        return OrderBookPhase(response)

    def _get_liquidity_band(self) -> int:
        """Get the liquidity band from the Order Book contract"""
        return self.contract.functions.getLiquidityBand().call()

    def _fetch_pre_trade_control_config(self) -> PreTradeControlConfig:
        """Fetch the trading pair Pre Trade Control Config from the Order Book contract"""
        response = self.contract.functions.getPreTradeControlConfig().call()

        return PreTradeControlConfig(
            max_value=response[0],
            min_value=response[1],
            price_collar_factor=response[2],
            max_matches=response[3],
        )

    def _get_static_ref_price(self) -> int:
        """Get the static reference price from the Order Book contract"""
        return self.contract.functions.getStaticRefPrice().call()

    def _get_volatility_management_config(self) -> VolatilityManagementConfig:
        """Get the volatility management config from the Order Book contract"""

        response = self.contract.functions.getVolatilityManagementConfig().call()

        return VolatilityManagementConfig(
            static_threshold=response[1],
            dynamic_threshold=response[2],
        )

    def _read_client_info(self):
        """Get Whitelist Info"""
        response = self.whitelist_contract.functions.readClientInfo(self.wallet).call()
        return ClientInfo(*response)

    def _await_base_allowance_tx(self, amount: int):
        """Set the allowance for the base token"""

        self.log.info("set base allowance to %s", amount)

        scaled_amount = self.upscale_quantity_native(amount)

        tx = self.base_contract.functions.approve(
            self.orderbook_addr,
            scaled_amount,
        ).build_transaction({"from": self.account.address})

        self._handle_transaction(tx)

    def _await_quote_allowance_tx(self, amount: int):
        """Set the allowance for the quote token"""

        self.log.info("set quote allowance to %s", amount)

        scaled_amount = self.upscale_price_native(amount)

        tx = self.quote_contract.functions.approve(
            self.orderbook_addr,
            scaled_amount,
        ).build_transaction({"from": self.account.address})

        self._handle_transaction(tx)

    def _await_buy_order_tx(self, quantity: Decimal, price: Decimal):
        """Create a buy order and wait for it's tx confirmation"""

        self.log.info(
            "create buy order with quantity %s and price %s",
            quantity,
            price,
        )

        order_data = self.encode_order_data(quantity, price)
        reporting_data = eth_abi.encode(["uint32", "uint32"], [0, 0])
        cross_identifier = eth_abi.encode(["uint32"], [0])

        tx = self.contract.functions.newBuyOrder(order_data, reporting_data, cross_identifier).build_transaction(
            {"from": self.account.address}
        )

        self._handle_transaction(tx)

    def _await_sell_order_tx(self, quantity: Decimal, price: Decimal):
        """Create a sell order and wait for it's tx confirmation"""

        self.log.info(
            "create sell order with quantity %s and price %s",
            quantity,
            price,
        )

        order_data = self.encode_order_data(quantity, price)
        reporting_data = eth_abi.encode(["uint32", "uint32"], [0, 0])
        cross_identifier = eth_abi.encode(["uint32"], [0])

        tx = self.contract.functions.newSellOrder(order_data, reporting_data, cross_identifier).build_transaction(
            {"from": self.account.address}
        )

        self._handle_transaction(tx)

    def _await_cancel_buy_orders_tx(self):
        """Cancel all buy orders and wait for it's tx confirmation"""

        if not self.admin:
            self.log.error("admin wallet not set, cannot cancel sell orders")
            return

        self.log.info("run admin batch cancel buy orders")
        tx = self.contract.functions.ownerBatchCancelBuyOrders(255).build_transaction({"from": self.admin.address})

        self._handle_transaction(tx)

    def _await_cancel_sell_orders_tx(self):
        """Cancel all sell orders and wait for it's tx confirmation"""

        if not self.admin:
            self.log.error("admin wallet not set, cannot cancel sell orders")
            return

        self.log.info("run admin batch cancel sell orders")
        tx = self.contract.functions.ownerBatchCancelSellOrders(255).build_transaction({"from": self.admin.address})

        self._handle_transaction(tx)

    ####################### ACTIONs #########################

    def set_base_allowance(self, amount: Decimal):
        self._await_base_allowance_tx(amount)

    def set_quote_allowance(self, amount: Decimal):
        self._await_quote_allowance_tx(amount)

    def get_balance(self) -> Pair:
        """Get the balance of the trading pair"""

        balance_of_base = self.base_contract.functions["balanceOf"]
        balance_of_quote = self.quote_contract.functions["balanceOf"]

        base_balance = balance_of_base(self.wallet).call()
        quote_balance = balance_of_quote(self.wallet).call()

        scaled_base_balance = self.downscale_quantity_native(base_balance)
        scaled_quote_balance = self.downscale_price_native(quote_balance)

        return Pair(scaled_base_balance, scaled_quote_balance)

    def create_buy_order(self, quantity: Decimal, price: Decimal, auto_allowance=True):
        """Create a buy order"""

        if auto_allowance:
            # first we set the appropriate allowance
            # amount to approve is calculated as the base of quantity and price
            # adding the commission
            amount = quantity * price
            amount_to_approve = amount + self.calculate_commission(amount)

            self._await_quote_allowance_tx(amount_to_approve)

        # then we create buy order transaction and wait for it to resolve
        self._await_buy_order_tx(quantity, price)

    def create_sell_order(self, quantity: Decimal, price: Decimal, auto_allowance=True):
        """Create a sell order"""

        if auto_allowance:
            # first we set the appropriate allowance
            # amount to approve is simply the quantity of the order
            self._await_base_allowance_tx(quantity)

        # then we create sell order transaction and wait for it to resolve
        self._await_sell_order_tx(quantity, price)

    def get_best_bid_offer(self) -> OrderBookOrders:
        """Get the best bid offer from the Order Book"""

        response = self.contract.functions.bestBidOffer().call()

        buy_data = (response >> 128) & util.LOWER128
        sell_data = response & util.LOWER128

        def as_pair(data: tuple[Decimal, Decimal]) -> Pair:
            return Pair(data[0], data[1])

        # decode order data and convert to pair
        buy_orders = [as_pair(self.decode_order_data(buy_data))]
        sell_orders = [as_pair(self.decode_order_data(sell_data))]

        return OrderBookOrders(buy_orders, sell_orders)

    def get_order_book_orders(self) -> OrderBookOrders:
        """Get the best offers from the Order Book"""

        response = self.contract.functions.bestFiftyOffers().call()

        def as_pair(data: tuple[Decimal, Decimal]) -> Pair:
            return Pair(data[0], data[1])

        # decode order data and convert to pair
        buy_orders = [as_pair(self.decode_order_data(x)) for x in response[0]]
        sell_orders = [as_pair(self.decode_order_data(x)) for x in response[1]]

        return OrderBookOrders(buy_orders, sell_orders)

    def get_order_book_order_count(self) -> OrderBookOrderCount:
        """Get the count of open orders"""

        buy_count = self.contract.functions.countBuyOrders().call()
        sell_count = self.contract.functions.countSellOrders().call()

        return OrderBookOrderCount(buy_count, sell_count)

    def fetch_dynamic_configuration(self):
        """Fetch the trading pair dynamic configuration from the Order Book contract"""

        return {
            "order_book_phase": self._get_order_book_phase(),
            "liquidity_band": self._get_liquidity_band(),
            "pre_trade_control_config": self._fetch_pre_trade_control_config(),
            "client_info": self._read_client_info(),
            "static_ref_price": self._get_static_ref_price(),
            "volatility_management_config": self._get_volatility_management_config(),
        }

    ####################### UTILS #######################

    def encode_order_data(self, quantity: Decimal, price: Decimal) -> bytes:
        """Encode order data for the Order Book contract"""

        if price < 0:
            raise ValueError(f"Order price {price} is below 0")

        if quantity < 0:
            raise ValueError(f"Order quantity {quantity} is below 0")

        scaled_price = self.upscale_price(price)
        scaled_quantity = self.upscale_quantity(quantity)

        order_data = eth_abi.encode(
            ["uint64", "uint64"],
            [scaled_quantity, scaled_price],
        )

        return order_data

    def decode_order_data(self, order_data: int) -> tuple[Decimal, Decimal]:
        """Decode order data for the Order Book contract"""
        price = order_data & util.LOWER64
        quantity = order_data >> 64 & util.LOWER64

        scaled_price = self.downscale_price(price)
        scaled_quantity = self.downscale_quantity(quantity)

        return (scaled_quantity, scaled_price)

    def upscale_price(self, price: Decimal) -> int:
        """Upscale price to the appropriate scale for the Order Book contract

        Args:
            price (Decimal): price of base to buy

        Returns:
            int: upscaled price
        """
        return int(self.config.quote_internal_scale * price)

    def upscale_price_native(self, price: Decimal) -> int:
        """Upscale price to the appropriate scale for the Order Book contract

        Args:
            price (Decimal): price of base to buy

        Returns:
            int: upscaled price
        """
        return int(self.config.quote_native_scale * price)

    def upscale_quantity(self, quantity: Decimal) -> int:
        """Upscale quantity to the appropriate scale for the Order Book contract

        Args:
            quantity (Decimal): quantity of base to buy

        Returns:
            int: upscaled quantity
        """
        return int(self.config.base_internal_scale * quantity)

    def upscale_quantity_native(self, quantity: Decimal) -> int:
        """Upscale quantity to the appropriate scale for the Order Book contract

        Args:
            quantity (Decimal): quantity of base to buy

        Returns:
            int: upscaled quantity
        """
        return int(self.config.base_native_scale * quantity)

    def downscale_price(self, price: int) -> Decimal:
        """Downscale price to the appropriate scale for the trading pair

        Args:
            price (int): price of base to buy

        Returns:
            Decimal: downscaled price
        """
        return Decimal(str(price)) / (self.config.quote_internal_scale)

    def downscale_price_native(self, price: int) -> Decimal:
        """Downscale price to the appropriate scale for the trading pair

        Args:
            price (int): price of base to buy

        Returns:
            Decimal: downscaled price
        """
        return Decimal(str(price)) / (self.config.quote_native_scale)

    def downscale_quantity(self, quantity: int) -> Decimal:
        """Downscale price to the appropriate scale for the trading pair

        Args:
            price (int): price of base to buy

        Returns:
            Decimal: downscaled price
        """
        return Decimal(str(quantity)) / (self.config.base_internal_scale)

    def downscale_quantity_native(self, quantity: int) -> Decimal:
        """Downscale quantity to the appropriate scale for the trading pair

        Args:
            quantity (int): quantity of base to buy

        Returns:
            Decimal: downscaled quantity
        """
        return Decimal(str(quantity)) / (self.config.base_native_scale)

    def calculate_commission(self, amount: Decimal) -> float:
        """Calculate the commission for a given amount

        Args:
            amount (Decimal): amount to calculate commission for

        Returns:
            float: commission amount in native quote scale
        """
        commission_denomination = 10**4

        return amount * self.config.taker_commission / (commission_denomination)
