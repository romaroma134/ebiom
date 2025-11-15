"""Real-time listener for PancakeSwap PairCreated events."""

import time
from typing import Callable, Dict

from web3 import Web3

from . import utils


class PairCreatedListener:
    def __init__(self, web3: Web3, callback: Callable[[Dict[str, str]], None], poll_interval: float = 2.0):
        self.web3 = web3
        self.callback = callback
        self.poll_interval = poll_interval
        self.contract = utils.get_contract(self.web3, utils.FACTORY_ADDRESS, utils.FACTORY_ABI)
        self.event_filter = self.contract.events.PairCreated.create_filter(fromBlock="latest")

    def run(self) -> None:
        while True:
            for event in self.event_filter.get_new_entries():
                data = {
                    "token0": event["args"]["token0"],
                    "token1": event["args"]["token1"],
                    "pair": event["args"]["pair"],
                }
                self.callback(data)
            time.sleep(self.poll_interval)
