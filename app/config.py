import os
import dotenv

dotenv.load_dotenv()

ARBITRUM_URL: str = os.environ["ARBITRUM_URL"]
ARBITRUM_NOVA_URL: str = os.environ["ARBITRUM_NOVA_URL"]
AMOUNT_LOW: float = float(os.environ["AMOUNT_LOW"])
AMOUNT_HIGH: float = float(os.environ["AMOUNT_HIGH"])

chains = {
    "nova": 42170,
    "arbitrum": 42161,
    "shardeum": 8082,
}

contracts_path = {
    "ERC20": "../contract/ERC20.json",
    "ERC721": "../contract/ERC721.json"
}

chain_tx_details = {

}


# chain_details = {
#     "chainId": 42161,
#     "gas": 250000,
#     "maxFeePerGas": Web3.toWei('0.1', 'gwei'),
#     "maxPriorityFeePerGas": Web3.toWei('0.1', 'gwei'),
# }