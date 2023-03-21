from board import Board
import sys


class Solver:

    def __init__(self, board: Board):
        self.board = board
        # init Z table
        self.__z = self.__create_z()

    # minimum distance of getting from node A to the target within cost T
    def z(self, a, t: int) -> int:
        return self.__z[t, a]

    # set of the shortest paths from node A to the target within a budget T
    def shortest_paths(self, a, t: int):
        current_distance = self.z(a, t)
        if a == self.board.peking:
            yield [a]
            return

        if current_distance >= sys.maxsize or t <= 0:
            return

        for b in self.board.graph.adj[a]:
            new_budget = t - self.board.graph.edges[a, b]['cost']
            if new_budget < 0:  # cannot afford
                continue
            new_distance = self.z(b, new_budget)
            if new_distance < current_distance:
                for p in self.shortest_paths(b, new_budget):
                    yield [a] + p

    def __create_z(self):
        z = dict()

        for tmpBudget in range(self.board.budget + 1):
            for node in self.board.graph.nodes():
                if node == self.board.peking:
                    z[tmpBudget, node] = 0
                    continue
                min_value = sys.maxsize
                for nbr, cost in self.board.possibleMoves(node):
                    if tmpBudget - cost >= 0:
                        new_length = z[tmpBudget - cost, nbr] + 1
                        min_value = min(min_value, new_length)
                z[tmpBudget, node] = min_value

        return z
