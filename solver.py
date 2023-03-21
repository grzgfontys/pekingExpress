from board import Board
import sys


class Solver:

    def __init__(self, board: Board):
        self.board = board
        # init Z table

    # minimum distance of getting from node A to the target within cost T
    def z(self, a, t: int) -> int:
        pass

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
