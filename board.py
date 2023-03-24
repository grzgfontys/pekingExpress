import json
import networkx as nx


class Board:
    def __init__(self, json_file, white_is_player: bool):
        # load the json data
        with open(json_file) as f:
            board = json.load(f)

        # Attributes storing game data
        road_data = board["Roads"]
        self.locationNumber = board["Locations"]["number"]
        self.critical_locations = board["Locations"]["critical"]
        self.start_node = board["StartLocation"]
        self.peking = 88
        self.starting_budget = board["Budget"]
        self.maxNodeNumber = (self.peking if self.peking > self.locationNumber else self.locationNumber) + 1
        self.computer_pos, self.player_pos = self.start_node, self.start_node
        self.computer_budget, self.player_budget = self.starting_budget, self.starting_budget
        self.computer_already_at_88, self.player_already_at_88 = 0, 0
        self.white_is_player = white_is_player

        # initialize graph
        self.graph = nx.DiGraph()
        for (i, src) in enumerate(road_data["a"]):
            (dst, cost) = (road_data["b"][i], road_data["price"][i])
            self.graph.add_edge(src, dst, cost=cost)

        # Add critical labels to the nodes
        for node in self.graph.nodes():
            self.graph.nodes[node]["critical"] = False
        for critical in self.critical_locations:
            self.graph.nodes[critical]["critical"] = True

        # Make graph undirected
        self.graph = self.graph.to_undirected()

    # Cost of travel between two nodes
    def cost(self, src, dst):
        return self.graph.edges[src, dst]['cost']

    # Possible moves for player position
    def possibleMovesPlayer(self):
        moves = dict()

        for nbr, datadict in self.graph.adj[self.player_pos].items():
            if self.graph.nodes[nbr]["critical"] and self.computer_pos == nbr:
                continue
            if self.player_budget is not None:
                if datadict["cost"] > self.player_budget:
                    continue
            moves[nbr] = datadict["cost"]

        return moves

    # Possible moves for computer position
    def possibleMoves(self, src):
        moves = []

        for nbr, datadict in self.graph.adj[src].items():
            moves.append((nbr, datadict["cost"]))

        return moves
    
    def update_computer_pos(self, new_pos):
        if new_pos == None:
            return
        for nbr, cost in self.possibleMoves(self.computer_pos):
            if nbr == new_pos:
                self.computer_budget -= cost
                self.computer_pos = new_pos
                break

    # Visualization of graph game/board using networkx
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
