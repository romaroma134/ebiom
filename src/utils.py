"""Utility helpers for interacting with PancakeSwap contracts."""

from functools import lru_cache
from typing import Any, Dict

from web3 import Web3
from web3.middleware import geth_poa_middleware


FACTORY_ADDRESS = Web3.to_checksum_address("0xCA143Ce32Fe78f1f7019d7d551a6402fC5350c73")
ROUTER_ADDRESS = Web3.to_checksum_address("0x10ED43C718714eb63d5aA57B78B54704E256024E")
WBNB_ADDRESS = Web3.to_checksum_address("0xBB4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")
BUSD_ADDRESS = Web3.to_checksum_address("0xe9e7cea3dedca5984780bafc599bd69add087d56")

FACTORY_ABI: list[Dict[str, Any]] = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "token0", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "token1", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "pair", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "name": "PairCreated",
        "type": "event",
    }
]

PAIR_ABI: list[Dict[str, Any]] = [
    {
        "inputs": [],
        "name": "getReserves",
        "outputs": [
            {"internalType": "uint112", "name": "_reserve0", "type": "uint112"},
            {"internalType": "uint112", "name": "_reserve1", "type": "uint112"},
            {"internalType": "uint32", "name": "_blockTimestampLast", "type": "uint32"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token0",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

ERC20_ABI: list[Dict[str, Any]] = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

ROUTER_ABI: list[Dict[str, Any]] = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
        ],
        "name": "getAmountsOut",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    }
]


def build_web3(wss_url: str) -> Web3:
    web3 = Web3(Web3.WebsocketProvider(wss_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3


def get_contract(web3: Web3, address: str, abi: list[Dict[str, Any]]):
    checksum = Web3.to_checksum_address(address)
    return web3.eth.contract(address=checksum, abi=abi)


@lru_cache(maxsize=256)
def get_token_symbol(web3: Web3, address: str) -> str:
    contract = get_contract(web3, address, ERC20_ABI)
    return contract.functions.symbol().call()


@lru_cache(maxsize=256)
def get_token_decimals(web3: Web3, address: str) -> int:
    contract = get_contract(web3, address, ERC20_ABI)
    return int(contract.functions.decimals().call())


def get_pair_reserves(web3: Web3, address: str) -> tuple[int, int]:
    contract = get_contract(web3, address, PAIR_ABI)
    reserves = contract.functions.getReserves().call()
    return int(reserves[0]), int(reserves[1])


def get_router(web3: Web3):
    return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)


def get_amounts_out(router, amount: int, path: list[str]) -> list[int]:
    return router.functions.getAmountsOut(amount, path).call()
