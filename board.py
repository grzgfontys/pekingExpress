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

        self.dpArray = self.createDPArray()

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

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):

        # Initialize minimum distance for next node
        min = sys.maxsize

        # -1 if there are no nodes left
        min_index = -1

        # Search not nearest vertex not in the
        # shortest path tree
        for u in range(self.maxNodeNumber):
            if dist[u][0] < min and sptSet[u] == False:
                min = dist[u][0]
                min_index = u

        return min_index

    def findShortestPath(self, src):
        dist = [(sys.maxsize, -1)] * self.maxNodeNumber
        dist[src] = (0, src)
        sptSet = [False] * self.maxNodeNumber

        for cout in range(self.maxNodeNumber):
            # if shortest path to node 88 was find there is no need to search more
            if sptSet[self.peking]:
                break

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # currentNode is always equal to src in first iteration
            currentNode = self.minDistance(dist, sptSet)


            # if there are no more nodes
            if currentNode == -1:
                break

            # Put the minimum distance vertex in the
            # shortest path tree
            sptSet[currentNode] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shortest path tree
            for nbr in self.possibleMoves(currentNode):
                if sptSet[nbr[0]] == False and dist[nbr[0]][0] > dist[currentNode][0] + nbr[1]:
                    dist[nbr[0]] = (dist[currentNode][0] + nbr[1], currentNode)
        nextNode = dist[self.peking]
        while dist[nextNode[0]][0] != src:
            nextNode = dist[nextNode[0]]
        return nextNode[1]
    
    def createDPArray(self):

        dp = [[sys.maxsize for j in range(self.maxNodeNumber+1)] for i in range(self.budget+1)]

        for i in range(self.budget+1):
            dp[i][self.peking] = 0

        q = deque()
        isPath = False
        q.append((self.peking, 0))

        while q:
            currentNode = q.popleft()


            for nbr in self.possibleMoves(currentNode[0]):
                for i in range(self.budget+1):
                    if dp[i][currentNode[0]] + nbr[1] <= i and dp[i][currentNode[0]] + nbr[1] <= dp[i][nbr[0]]:
                        dp[i][nbr[0]] = dp[i][currentNode[0]] + nbr[1]
                        isPath = True

                if isPath:
                    q.append(nbr)
                    isPath = False

        fin = True