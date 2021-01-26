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
    return json.loads(body)


def get_last_n_transactions(raw_block, n=None):
    out = []
    if n:
        for i in range(n):
            out.append(raw_block['tx'][i])
    else:
        out = raw_block['tx']
    return out


def extract_to_addresses(transaction):
    addresses = []
    out = transaction["out"]
    for x in out:
        if x["value"] != 0:
            addresses.append((x["addr"], x["value"]))
    return addresses
