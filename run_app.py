from app.main import deploy_contract

if __name__ == "__main__":
    """
    contract_name - possible variants - ERC20, ERC721, CryptoSchool
    network - possible variants - nova, arbitrum
    """
    deploy_contract("ERC20", "nova")
