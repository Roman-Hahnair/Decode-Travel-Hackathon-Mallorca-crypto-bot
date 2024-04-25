from web3 import Web3
from web3.middleware import geth_poa_middleware
import os

# Read the ABI from a file
with open("contract_abi.json", "r") as file:
    abi_str = file.read()

#contract_address = "0x95EBB9Bc87F739EB2A6057Cd0707AAEf3936DE97"
contract_address = "0x252d1735ccc7E14F0DBA89162487f0EeB1A170ec"

private_key = os.getenv('CRYPTO_PRIVATE_KEY')

#sample_image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-BPqH6tWWgHOUicO8Wwjqvukg/user-7eSJt0pSU95AQ0mS2VKwDATk/img-L1sVCvwD0RTVWr70EbnJBjFW.png?st=2024-04-24T15%3A11%3A11Z&se=2024-04-24T17%3A11%3A11Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-24T14%3A53%3A27Z&ske=2024-04-25T14%3A53%3A27Z&sks=b&skv=2021-08-06&sig=0yc78zgl2jNyyCFJZnPMv159NpuE2fD/pc3a1xjgrkQ%3D"
#sample_image_url = "ipfs/QmehXwcBKsHZoS8AUK6d1RxQnvvwrysLoX1oAkayeSzXyJ/4.webp"

client_url = "https://columbus.camino.network/ext/bc/C/rpc"


# Initialize the Web3 client
web3 = Web3(Web3.HTTPProvider(client_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Contract address and ABI
contract_address = Web3.to_checksum_address(contract_address)
contract_abi = abi_str

# Connect to the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def main():
    try:

        #account = web3.eth.account.privateKeyToAccount(private_key)
        #public_address = account.address

        account = web3.eth.account.from_key(private_key)
        public_address = account.address

        # Replace these with the actual values you want to use
        gpsCoordinates = "0,0"          # Replace with actual GPS coordinates
        sponsorshipLength = 1           # Replace with actual sponsorship length
        area = 1                        # Replace with actual area
        
        # Update the 'mint' function call with the actual parameters
        tx_hash = contract.functions.mint(
            public_address,  # address
            sample_image_url,  # string (tokenURI)
            gpsCoordinates,  # string (gpsCoordinates)
            sponsorshipLength,  # uint256 (sponsorshipLength)
            area  # uint256 (area)
        ).transact({'from': public_address})  # The account making the transaction
        
        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print("Success! Transaction hash:", receipt.transactionHash.hex())
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
