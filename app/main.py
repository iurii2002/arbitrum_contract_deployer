"""
Dev: https://t.me/python_web3
"""

import json
import random
import requests
from pathlib import Path
from random import randint, uniform
from time import sleep

from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from loguru import logger
from typing import List
from web3 import Account, Web3
from web3.contract import Contract
from web3.types import ABI

from app.config import AMOUNT_HIGH, AMOUNT_LOW, ARBITRUM_URL, ARBITRUM_NOVA_URL
from app.config import contracts_path, chains

logger.add(
    "log/debug.log",
    format="{time} | {level} | {message}",
    level="DEBUG",
)


#
# def send_eth_to_contract(wallet: LocalAccount, to_address: str, amount: float) -> None:
#     """Отправка указанного количества эфиров на контракт."""
#
#     dict_transaction = {
#         "chainId": w3.eth.chain_id,
#         "from": wallet.address,
#         "to": w3.toChecksumAddress(to_address),
#         "value": w3.toWei(amount, "ether"),
#         "gas": 300_000,
#         "gasPrice": w3.eth.gas_price,
#         "nonce": w3.eth.getTransactionCount(wallet.address),
#     }
#
#     signed_txn = wallet.sign_transaction(dict_transaction)
#     txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
#     logger.info(
#         f"Send {amount} eth to {to_address}, transaction: {txn_hash.hex()}")

#
# def return_eth_from_contract(
#     wallet: LocalAccount, contract_address: str, abi: ABI
# ) -> None:
#     """Возврат всего баланса из контракта на кошелёк-создатель."""
#
#     dict_transaction = {
#         "chainId": w3.eth.chain_id,
#         "from": wallet.address,
#         "value": 0,
#         "gas": 500_000,
#         "gasPrice": w3.eth.gas_price,
#         "nonce": w3.eth.getTransactionCount(wallet.address),
#     }
#
#     contract = w3.eth.contract(
#         address=w3.toChecksumAddress(contract_address), abi=abi)
#
#     transaction = contract.functions.MoneyBack().buildTransaction(dict_transaction)
#     signed_txn = wallet.sign_transaction(transaction)
#
#     txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
#     logger.info(
#         f"Return balance from contract, transaction: {txn_hash.hex()}.")
#
#

#
#


#
#
# def main() -> None:
#
#
#     wallets = load_wallets()
#     logger.info("Load wallets.")
#
#     bytecode = load_bytecode()

#
#     contract = w3.eth.contract(
#         bytecode=bytecode,
#         abi=json.load(Path("./contract/contract_abi.json").open())
#     )
#
#     for i, wallet in enumerate(wallets):
#         txn_hash = deploy_contract(wallet, contract)
#         sleep(randint(20, 40))
#
#         contract_address = w3.eth.get_transaction_receipt(
#             txn_hash).contractAddress
#
#         send_eth_to_contract(
#             wallet=wallet,
#             to_address=contract_address,
#             amount=uniform(AMOUNT_LOW, AMOUNT_HIGH),
#         )
#
#         sleep(randint(10, 20))
#
#         return_eth_from_contract(wallet, contract_address, contract.abi)
#
#         logger.success(f"{i+1}/{len(wallets)}")
#
#     logger.success("Finish.")

def load_bytecode(contract_name) -> str:
    return json.load(Path(contracts_path[contract_name]).open())['bytecode']['object'][2:]


def load_abi(contract_name) -> str:
    return json.load(Path(contracts_path[contract_name]).open())['abi']


def _deploy_contract(w3, wallet, contract, *args):

    transaction = contract.constructor(*args).buildTransaction(
        {
            "chainId": chains['nova'],
            "gasPrice": w3.toWei(0.0000000001, "ether"),
            "gas": 1000000,
            "from": wallet.address,
            "value": 0,
            "nonce": w3.eth.getTransactionCount(wallet.address)
        }
    )

    signed_txn = wallet.sign_transaction(transaction)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(
        f"Deploy contract by {wallet.address}, transaction: {txn_hash.hex()}.")
    return txn_hash


def set_network(network: str):
    w3 = Web3(Web3.HTTPProvider(network))
    return w3


def load_wallets():
    """Загрузка кошельков из текстовика."""
    file = Path("./wallets.txt").open()
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def get_random_word():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.splitlines()
    word = random.choice(words).decode("utf-8")
    return word


def deploy_contract(private_key: str, contract_name: str, network: str):
    """
    contract_name - possible variants - ERC20, ERC721, CryptoSchool
    network - possible variants - ARBITRUM_URL, ARBITRUM_NOVA_URL
    """
    logger.info(f"Start in network {network}.")
    w3 = set_network(network)
    accounts = load_wallets()
    logger.info(f"Loaded {len(accounts)} accounts")
    bytecode = load_bytecode(contract_name)
    logger.info("Loaded bytecode")
    abi = load_abi(contract_name)
    logger.info("Loaded abi")


    contract = w3.eth.contract(
        abi=abi,
        bytecode=bytecode)

    for account in accounts:

        # DEPLOY ERC20. UNCOMMENT TO DEPLOY
        random_word = get_random_word()
        name = random_word + " token"
        symbol = random_word[:3].capitalize()
        amount = 100 * random.randint(10, 10000) * (10**18)
        _deploy_contract(w3, account, contract, name, symbol, amount)

        ## DEPLOY ERC721. UNCOMMENT TO DEPLOY
        # random_word = get_random_word()
        # name = random_word + " token"
        # symbol = random_word[:3].capitalize()
        # _deploy_contract(w3, account, contract, name, symbol)

        ## DEPLOY CryptoSchool. UNCOMMENT TO DEPLOY
        # _deploy_contract(w3, account, contract)
