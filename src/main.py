"""Entry point for the BSC pair radar."""

import datetime
from typing import Dict

from .filters import LiquidityFilter
from .listener import PairCreatedListener
from . import utils

BSC_WSS_URL = "wss://bsc-ws-node.nariox.org:443"


def handle_pair(pair_data: Dict[str, str], liquidity_filter: LiquidityFilter) -> None:
    info = liquidity_filter.evaluate(pair_data)
    if not info:
        return
    timestamp = datetime.datetime.utcnow().isoformat()
    print(
        " | ".join(
            [
                f"time: {timestamp}",
                f"pair: {info.pair_address}",
                f"token0: {info.symbol0} ({info.token0})",
                f"token1: {info.symbol1} ({info.token1})",
                f"liquidity_usd: {info.usd_liquidity:,.2f}",
                f"liquidity_bnb: {info.bnb_liquidity:,.4f}",
            ]
        )
    )


def main() -> None:
    web3 = utils.build_web3(BSC_WSS_URL)
    router = utils.get_router(web3)
    liquidity_filter = LiquidityFilter(web3, router)

    def callback(data: Dict[str, str]) -> None:
        handle_pair(data, liquidity_filter)

    listener = PairCreatedListener(web3, callback)
    listener.run()


if __name__ == "__main__":
    main()
