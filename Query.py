import requests
import json


def get_latest_block_hash():
    body = requests.get('https://blockchain.info/latestblock').content.decode('utf-8')
    return json.loads(body)['hash']


def get_raw_block(block_hash):
    block = requests.get('https://blockchain.info/rawblock/' + block_hash).content.decode('utf-8')
    return json.loads(block)


def get_raw_address(address_hash):
    body = requests.get('https://blockchain.info/rawaddr/' + address_hash).content.decode('utf-8')
    return json.load(body)


def get_last_n_transactions(raw_block, n):
    out = []
    for i in range(n):
        out.append(raw_block['tx'][i])
    return out


print(get_latest_block_hash())

example_block = get_raw_block(get_latest_block_hash())

for transaction in get_last_n_transactions(example_block, 3):
    print(transaction)

