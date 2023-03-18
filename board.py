import networkx as nx
import json
import matplotlib.pyplot as plt


class Board:
    def __init__(self, json_file):
        with open(json_file) as f:
            board = json.load(f)

        self.graph = nx.DiGraph()

        # initialize graph
        self.critical_locations = board["locations"]["critical"]
        road_data = board["roads"]
        for (i, src) in enumerate(road_data["source"]):
            (dst, cost) = (road_data["target"][i], road_data["price"][i])
            self.graph.add_edge(src, dst, cost=cost)

        self.start_node = board["startLocation"]
        self.target_node = 88
        self.budget = board["budget"]

    def visualize(self):
        layout = nx.spring_layout(self.graph, seed=2137)
        nx.draw_networkx_nodes(self.graph, layout)
        nx.draw_networkx_edges(self.graph, layout)

        # labels
        nx.draw_networkx_labels(self.graph, layout)
        edge_labels = nx.get_edge_attributes(self.graph, "cost")
        nx.draw_networkx_edge_labels(self.graph, layout, edge_labels)
