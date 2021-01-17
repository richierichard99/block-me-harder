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


def get_last_n_transactions(raw_block, n=None):
    out = []
    if n:
        for i in range(n):
            out.append(raw_block['tx'][i])
    else:
        out = raw_block['tx']
    return out


def extract_to_addresses(transaction):
    addresses = set()
    out = transaction["out"]
    for x in out:
        if x["value"] != 0:
            addresses.add(x["addr"])
    return addresses


def transaction_edges_nodes(raw_block, n=None):
    edges = []
    nodes = []
    for transaction in get_last_n_transactions(raw_block, n):
        nodes.append((transaction["hash"], {"color": "red"}))
        for address in extract_to_addresses(transaction):
            edges.append((transaction["hash"], address))
            nodes.append((address, {"color": "blue"}))
    return edges, nodes



# def groupAndSortAddresses()


print(get_latest_block_hash())

example_block = get_raw_block(get_latest_block_hash())

print("/// EDGES ////")
edges, nodes = transaction_edges_nodes(example_block)
G = nx.Graph()
G.add_edges_from(edges)
G.add_nodes_from(nodes)

color_map = []
for node in G.nodes(data=True):
    color_map.append(node[1]["color"])

plt.axis("off")
nx.draw(G, node_color=color_map, with_labels=False)
plt.show()




