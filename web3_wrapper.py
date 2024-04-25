from web3 import Web3
from web3.middleware import geth_poa_middleware
import os

# Read the ABI from a file
with open("contract_abi.json", "r") as file:
    abi_str = file.read()

contract_address = "0x252d1735ccc7E14F0DBA89162487f0EeB1A170ec"

private_key = os.getenv("CRYPTO_PRIVATE_KEY")

# sample_image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-BPqH6tWWgHOUicO8Wwjqvukg/user-7eSJt0pSU95AQ0mS2VKwDATk/img-L1sVCvwD0RTVWr70EbnJBjFW.png?st=2024-04-24T15%3A11%3A11Z&se=2024-04-24T17%3A11%3A11Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-24T14%3A53%3A27Z&ske=2024-04-25T14%3A53%3A27Z&sks=b&skv=2021-08-06&sig=0yc78zgl2jNyyCFJZnPMv159NpuE2fD/pc3a1xjgrkQ%3D"
sample_image_url = "ipfs/QmehXwcBKsHZoS8AUK6d1RxQnvvwrysLoX1oAkayeSzXyJ/4.webp"

client_url = "https://columbus.camino.network/ext/bc/C/rpc"

# Initialize the Web3 client
web3 = Web3(Web3.HTTPProvider(client_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract address and ABI
# contract_address_cs = Web3.toChecksumAddress(contract_address)
contract_address_cs = Web3.to_checksum_address(contract_address)


contract_abi = abi_str

# Connect to the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


import re

def is_valid_ethereum_address(address):
    """
    Checks if the given string is a valid Ethereum address.

    This function uses the re.fullmatch method to ensure the entire string matches the Ethereum address pattern. It checks:

    Whether the string starts with '0x'.
    Followed by exactly 40 characters which must be hexadecimal (consisting of digits and letters from A to F, case insensitive).    

    Args:
    address (str): The address to check.

    Returns:
    bool: True if the address is valid, False otherwise.
    """
    if isinstance(address, str) and re.fullmatch(r"0x[a-fA-F0-9]{40}", address):
        return True
    return False


def update_report(msg, report):
    print(msg)
    report += msg + "\n"
    return report


def mint_nft(address_to):
    report = ""
    success7 = False

    try:
        if private_key is None:
            report = update_report("ERROR! Private key is None...", report)
 

        account = web3.eth.account.from_key(private_key)
        public_address = account.address
        fromAddr = Web3.to_checksum_address(public_address)

        address_to = Web3.to_checksum_address(address_to)
        #address_to = (
        #    "0x6e339091198CdfbAfE5942e8d4198aC7F84b470e"  ## TODO make it variable
        #)

        dueTime = 1716624349

        # Replace these with the actual values you want to use
        gpsCoordinates = "0,0"  # Replace with actual GPS coordinates
        sponsorshipLength = 1  # Replace with actual sponsorship length
        area = 1  # Replace with actual area

        nonce = web3.eth.get_transaction_count(public_address)

        report = update_report("Preparing tx...", report)

        tx_hash = contract.functions.mint(
            address_to,  # address to send nft to
            sample_image_url,  # string (tokenURI)
            gpsCoordinates,  # string (gpsCoordinates)
            sponsorshipLength,  # uint256 (sponsorshipLength)
            area,  # uint256 (area)
            dueTime,  # duedate
        ).build_transaction(
            {"from": fromAddr, "nonce": nonce, "chainId": 501}
        )  # The account making the transaction

        signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)

        report = update_report("tx signed...", report)

        send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        report = update_report("tx sent...", report)

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(send_tx)

        msg = "Success! Transaction hash: " + str(receipt.transactionHash.hex())
        report = update_report(msg, report)

        success7 = True

    except Exception as e:
        # print("An error occurred:", e)
        msg = "An error occurred: " + str(e)
        report = update_report(msg, report)

    return success7, report


if __name__ == "__main__":
    mint_nft("0x6e339091198CdfbAfE5942e8d4198aC7F84b470e")
