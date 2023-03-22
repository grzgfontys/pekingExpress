import sys
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Board:
    def __init__(self, json_file):
        # load the json data
        with open(json_file) as f:
            board = json.load(f)

        road_data = board["roads"]
        self.locationNumber = board["locations"]["number"]
        self.critical_locations = board["locations"]["critical"]
        self.start_node = board["startLocation"]
        self.peking = 88
        self.budget = board["budget"]
        self.maxNodeNumber = (self.peking if self.peking > self.locationNumber else self.locationNumber) + 1
        self.dpArray = []

        # initialize graph
        self.graph = nx.DiGraph()
        for (i, src) in enumerate(road_data["source"]):
            (dst, cost) = (road_data["target"][i], road_data["price"][i])
            self.graph.add_edge(src, dst, cost=cost)

        self.graph = self.graph.to_undirected()

        for critical in self.critical_locations:
            self.graph.nodes[critical]["critical"] = True

    def cost(self, src, dst):
        return self.graph.edges[src, dst]['cost']

    def possibleMovesString(self, position):
        moves = []

        for nbr, datadict in self.graph.adj[position].items():
            moves.append(f"Move to {nbr} with cost of { datadict['cost']}")

        return moves

    def possibleMoves(self, src):
        moves = []

        for nbr, datadict in self.graph.adj[src].items():
            moves.append((nbr, datadict["cost"]))

        return moves

    def visualize(self):
        layout = nx.spring_layout(self.graph, seed=2137)
        nx.draw_networkx_nodes(self.graph, layout)
        nx.draw_networkx_edges(self.graph, layout)

        # labels
        nx.draw_networkx_labels(self.graph, layout)
        # edge cost
        edge_labels = nx.get_edge_attributes(self.graph, "cost")
        nx.draw_networkx_edge_labels(self.graph, layout, edge_labels)
        # nodes critical locations
        node_labels = nx.get_node_attributes(self.graph, "critical")
        nx.draw_networkx_labels(
            self.graph, layout, node_labels, verticalalignment="bottom")
