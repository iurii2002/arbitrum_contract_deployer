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

networks_url = {
    'nova': ARBITRUM_NOVA_URL,
    'arbitrum': ARBITRUM_URL,
}

contracts_path = {
    "ERC20": "contract/ERC20.json",
    "ERC721": "contract/ERC721.json"
}
