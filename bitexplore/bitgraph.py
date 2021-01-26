import networkx as nx
import matplotlib.pyplot as plt
import bitquery as bq


class BitGraph:
    def __init__(self, transactions):
        self.transactions = transactions
        self.edges, self.nodes = self.get_edges_nodes()
        self.graph, self.options = self.build_graph()

    def get_edges_nodes(self):
        edges = []
        nodes = []
        for transaction in self.transactions:
            nodes.append((transaction["hash"], {"color": "red"}))
            for address in bq.extract_to_addresses(transaction):
                edges.append((transaction["hash"], address[0], {"amount": address[1]}))
                nodes.append((address[0], {"color": "blue"}))
        return edges, nodes

    def build_graph(self):
        graph = nx.Graph()
        graph.add_edges_from(self.edges)
        graph.add_nodes_from(self.nodes)

        node_colors = [node[1]["color"] for node in graph.nodes(data=True)]
        # edge_colors = [edge[2]["amount"] for edge in graph.edges(data=True)]

        options = {
            # '"edge_color": edge_colors,
            "node_color": node_colors,
            "width": 2,
            # "edge_cmap": plt.cm.Blues,
            "with_labels": False,
        }

        return graph, options

    def visualise(self):
        plt.axis("off")
        nx.draw(self.graph, **self.options)
        plt.show()


if __name__ == '__main__':
    latest_block = bq.get_latest_block_hash()
    transactions = bq.get_raw_block(latest_block)["tx"]

    btc_graph = BitGraph(transactions)
    btc_graph.visualise()
