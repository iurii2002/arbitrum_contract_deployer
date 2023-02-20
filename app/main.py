import json
import random
import time

import requests

from pathlib import Path
from hexbytes import HexBytes
from loguru import logger
from typing import List
from web3 import Account, Web3
from eth_account.signers.local import LocalAccount

from app.config import contracts_path, chain_gas, networks_url

logger.add(
    "log/debug.log",
    format="{time} | {level} | {message}",
    level="DEBUG",
)


def load_bytecode(contract_name) -> str:
    return json.load(Path(contracts_path[contract_name]).open())['bytecode']['object'][2:]


def load_abi(contract_name) -> str:
    return json.load(Path(contracts_path[contract_name]).open())['abi']


def _deploy_contract(w3, wallet, contract, *args) -> HexBytes:

    transaction = contract.constructor(*args).buildTransaction(
        {
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "gas": chain_gas[w3.eth.chain_id],
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


def set_network(network: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(networks_url[network]))
    return w3


def load_wallets() -> List[LocalAccount]:
    """Загрузка кошельков из текстовика."""
    file = Path("app/wallets.txt").open()
    return [Account.from_key(line.replace("\n", "")) for line in file.readlines()]


def get_random_word():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.splitlines()
    word = random.choice(words).decode("utf-8")
    return word


def deploy_contract(contract_name: str, network: str) -> None:
    try:
        """
        contract_name - possible variants - ERC20, ERC721, CryptoSchool
        network - possible variants - nova, arbitrum
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
            try:
                # if w3.eth.get_balance(account.address) < Web3.toWei(0.001, 'ether'):
                #     logger.error(f"not enough bvalance on wallet {account.address}")
                #     continue

                txn_hash = None
                if contract_name == "ERC20":
                    random_word = get_random_word().capitalize()
                    name = random_word + " token"
                    symbol = random_word[:3].upper()
                    amount = 10 ** random.randint(1, 10) * (10**18)
                    txn_hash = _deploy_contract(w3, account, contract, name, symbol, amount)

                elif contract_name == "ERC721":
                    random_word = get_random_word()
                    name = random_word + " token"
                    symbol = random_word[:3].capitalize()
                    txn_hash = _deploy_contract(w3, account, contract, name, symbol)

                elif contract_name == "CryptoSchool":
                    txn_hash = _deploy_contract(w3, account, contract)

                else:
                    logger.error("Wrong contract name, please use correct one")

                if txn_hash is not None:
                    logger.info("Waiting 5 seconds until transaction is minted")
                    time.sleep(5)
                    contract_address = w3.eth.get_transaction_receipt(
                        txn_hash).contractAddress
                    logger.info(f"Deployed contract with the address {contract_address}")
            except Exception as err:
                logger.error(f"Account account {err}")

        logger.info("Finished")
    except Exception as err:
        logger.error(err)
