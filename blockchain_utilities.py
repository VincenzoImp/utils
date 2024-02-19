from web3 import Web3
import requests
import time
from fake_useragent import UserAgent
from web3.middleware import geth_poa_middleware

infura_api = 'e0a4e987f3ff4f4fa9aa21bb08f09ef5'
etherscan_api = '1FKT3JVMPXKD91HGEUID16AMAC1D8DQF4N'
bscscan_api = 'NCB92W9D7B9BFHIBSZ9Y44RADAZP4ICQFF'

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            },
            {
                "name": "_spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]


def get_normal_txs(address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs

def get_internal_txs(address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=txlistinternal&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs

def get_erc20_txs(address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs

def get_erc721_txs(address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=tokennfttx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=tokennfttx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs

def get_erc1155_txs(address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=token1155tx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=token1155tx&address={address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs

def get_account_transactions(address, chain):
    txs = {}
    txs['normal'] = get_normal_txs(address, chain)
    txs['internal'] = get_internal_txs(address, chain)
    txs['erc20'] = get_erc20_txs(address, chain)
    txs['erc721'] = get_erc721_txs(address, chain)
    txs['erc1155'] = get_erc1155_txs(address, chain)
    return txs






# def get_token_transactions(token_address, chain):

#     def get_new_transactions(results, token_address, starting_block_number, chain):
#             time.sleep(0.2)
#             if chain == 'ethereum':
#                 endpoint = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock={starting_block_number}&endblock=999999999&sort=asc&apikey={etherscan_api}"
#             elif chain == 'binance-smart-chain':
#                 endpoint = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock={starting_block_number}&endblock=999999999&sort=asc&apikey={bscscan_api}"
#             response = requests.get(endpoint)
#             data = response.json()
#             if len(data['result']) > 0:
#                 results += data['result']
#             return results, len(data['result']), data['result'][-1]['blockNumber']

#     results = []
#     current_total_transaction = 0
#     time.sleep(0.2)
#     if chain == 'ethereum':
#         endpoint = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock=0&endblock=999999999&sort=asc&apikey={etherscan_api}"
#     elif chain == 'binance-smart-chain':
#         endpoint = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock=0&endblock=999999999&sort=asc&apikey={bscscan_api}"
#     response = requests.get(endpoint)
#     data = response.json()
#     if len(data['result']) > 0:
#         current_total_transaction += len(data['result'])
#         results += data['result']
#         ntransactions = len(data['result'])
#         starting_block_number = data['result'][-1]['blockNumber']
#         while ntransactions == 10000:
#             results, ntransactions, starting_block_number = get_new_transactions(results, token_address, starting_block_number, chain)
#             current_total_transaction += ntransactions
#     return results


def get_token_transactions(token_address, chain):
    txs = []
    startblock = 0
    time.sleep(0.2)
    while True:
        if chain == 'ethereum':
            url = f"https://api.etherscan.io/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={etherscan_api}"
        elif chain == 'binance-smart-chain':
            url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={token_address}&page=1&startblock={startblock}&endblock=999999999&sort=asc&apikey={bscscan_api}"
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(url, headers=headers)
        data = response.json()
        txs += data['result']
        if len(data['result']) < 10000:
            break
        startblock = data['result'][-1]['blockNumber']
    new_txs = []
    for tx in txs:
        if tx not in new_txs:
            new_txs.append(tx)
    txs = sorted(new_txs, key=lambda x: x['timeStamp'])
    return txs


def get_contract_creation(address, chain):
    if chain == 'ethereum':
        url = f'https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses={address}&apikey={etherscan_api}'
    elif chain == 'binance-smart-chain':
        url = f'https://api.bscscan.com/api?module=contract&action=getcontractcreation&contractaddresses={address}&apikey={bscscan_api}'
    time.sleep(0.2)
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    responce = requests.get(url, headers=headers).json()
    if responce['status'] == '1':
        return responce['result'][0]
    return None

    




def get_w3(query_mode='http', chain='eth'):
    data = {
        'eth': {
            'rpc': '',
            'http': 'https://eth.public-rpc.com'
        },
        'bsc': {
            'rpc': '',
            # 'http': 'https://1rpc.io/bnb'
            'http': 'https://bsc-dataseed1.binance.org/'
        }
    }
    tmp = data[chain][query_mode]
    w3_data = {
        'eth': {
            'rpc': Web3(Web3.IPCProvider(tmp)),
            'http': Web3(Web3.HTTPProvider(tmp))
        },
        'bsc': {
            'rpc': Web3(Web3.IPCProvider(tmp)),
            'http': Web3(Web3.HTTPProvider(tmp))
        }
    }
    if query_mode == 'http' and chain == 'bsc':
        web3_binance = Web3(Web3.HTTPProvider(('https://bsc-dataseed1.binance.org/')))
        web3_binance.middleware_onion.inject(geth_poa_middleware, layer=0)
        return web3_binance
    return w3_data[chain][query_mode]