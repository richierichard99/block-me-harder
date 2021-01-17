import requests
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def get_latest_block_hash():
    body = requests.get('https://blockchain.info/latestblock').content.decode('utf-8')
    return json.loads(body)['hash']


def get_raw_block(block_hash):
    block = requests.get('https://blockchain.info/rawblock/' + block_hash).content.decode('utf-8')
    return json.loads(block)


def get_raw_address(address_hash):
    body = requests.get('https://blockchain.info/rawaddr/' + address_hash).content.decode('utf-8')
    return json.loads(body)


def get_last_n_transactions(raw_block, n):
    out = []
    for i in range(n):
        out.append(raw_block['tx'][i])
    return out


def extract_to_addresses(transaction):
    addresses = set()
    out = transaction["out"]
    for x in out:
        if x["value"] != 0:
            addresses.add(x["addr"])
    return addresses


def transaction_edges_nodes(raw_block, n):
    edges = set()
    nodes = set()
    for transaction in get_last_n_transactions(raw_block, n):
        nodes.add(transaction["hash"])
        for address in extract_to_addresses(transaction):
            edges.add((transaction["hash"], address))
            nodes.add(address)
    return edges, nodes



# def groupAndSortAddresses()


print(get_latest_block_hash())

example_block = get_raw_block(get_latest_block_hash())

print("/// EDGES ////")
edges, nodes = transaction_edges_nodes(example_block, 20)
G = nx.Graph()
G.add_edges_from(edges)
G.add_nodes_from(nodes)

plt.axis("off")
nx.draw(G)
plt.show()




