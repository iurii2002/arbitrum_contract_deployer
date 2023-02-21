import os
import dotenv

dotenv.load_dotenv()

ARBITRUM_URL: str = os.environ["ARBITRUM_URL"]
ARBITRUM_NOVA_URL: str = os.environ["ARBITRUM_NOVA_URL"]
SHARDEUM_URL: str = os.environ["SHARDEUM_URL"]

chains = {
    "nova": 42170,
    "arbitrum": 42161,
    "shardeum": 8082,
}

networks_url = {
    'nova': ARBITRUM_NOVA_URL,
    'arbitrum': ARBITRUM_URL,
    'shardeum': SHARDEUM_URL,
}

chain_gas = {
    42170: 5000000,
    42161: 20000000,
    8082: 2000000,
}

contracts_path = {
    "ERC20": "contract/ERC20.json",
    "ERC721": "contract/ERC721.json",
    "CryptoSchool": "contract/CryptoSchool.json",
}
