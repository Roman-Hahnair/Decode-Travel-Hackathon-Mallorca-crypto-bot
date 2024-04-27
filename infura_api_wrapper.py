import requests
import json
import os

"""
Here we experimented with using the Infura API to work with the Avalanche.
It works, seems one can delegate much of the low-level blockhain stuff to it. 
Could be useful for other projects. 

https://docs.infura.io/api/networks/avalanche-c-chain/quickstart
"""


api_key = os.getenv('INFURA_API_TOKEN')

url = f'https://avalanche-mainnet.infura.io/v3/{api_key}'

payload = {
    "jsonrpc": "2.0",
    "method": "eth_blockNumber",
    "params": [],
    "id": 1
}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers).json()

print(response)