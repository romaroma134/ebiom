"""Filtering utilities for PancakeSwap pairs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from web3 import Web3

from . import utils


@dataclass
class PairInfo:
    pair_address: str
    token0: str
    token1: str
    symbol0: str
    symbol1: str
    bnb_liquidity: float
    usd_liquidity: float


class LiquidityFilter:
    def __init__(self, web3: Web3, router, usd_threshold: float = 1000.0):
        self.web3 = web3
        self.router = router
        self.usd_threshold = usd_threshold

    def evaluate(self, pair_data: Dict[str, str]) -> Optional[PairInfo]:
        pair_address = Web3.to_checksum_address(pair_data["pair"])
        token0 = Web3.to_checksum_address(pair_data["token0"])
        token1 = Web3.to_checksum_address(pair_data["token1"])
        reserve0, reserve1 = utils.get_pair_reserves(self.web3, pair_address)
        bnb_total = self._reserve_to_bnb(token0, reserve0) + self._reserve_to_bnb(token1, reserve1)
        bnb_price = self._get_wbnb_price_usd()
        usd_total = bnb_total * bnb_price
        if usd_total < self.usd_threshold:
            return None
        symbol0 = utils.get_token_symbol(self.web3, token0)
        symbol1 = utils.get_token_symbol(self.web3, token1)
        return PairInfo(
            pair_address=pair_address,
            token0=token0,
            token1=token1,
            symbol0=symbol0,
            symbol1=symbol1,
            bnb_liquidity=bnb_total,
            usd_liquidity=usd_total,
        )

    def _reserve_to_bnb(self, token_address: str, reserve: int) -> float:
        if reserve == 0:
            return 0.0
        if token_address.lower() == utils.WBNB_ADDRESS.lower():
            return reserve / 10 ** utils.get_token_decimals(self.web3, token_address)
        try:
            path = [token_address, utils.WBNB_ADDRESS]
            amounts_out = utils.get_amounts_out(self.router, reserve, path)
            return amounts_out[-1] / 10 ** 18
        except Exception:
            return 0.0

    def _get_wbnb_price_usd(self) -> float:
        amount_in = 10 ** 18
        try:
            amounts_out = utils.get_amounts_out(self.router, amount_in, [utils.WBNB_ADDRESS, utils.BUSD_ADDRESS])
            return amounts_out[-1] / 10 ** 18
        except Exception:
            return 0.0
