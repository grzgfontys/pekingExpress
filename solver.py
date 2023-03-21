from board import Board
import sys

class Solver:

    def __init__(self, board: Board):
        self.board = board
        # init Z table
        self.z = self.createZ

    # minimum distance of getting from node A to the target within cost T
    def z(self, a, t: int):
        pass

    def shortest_paths(self, a, t: int):
        pass

    def createZ(self):
        # z = [[sys.maxsize for j in range(self.board.maxNodeNumber)] for i in range(self.board.budget+1)]
        z = dict()

        for tmpBudget in range(self.board.budget+1):
            for node in self.board.graph.nodes():
                if(node == self.board.peking):
                    z[tmpBudget, node] = 0
                    continue
                min_value = sys.maxsize
                for nbr, cost in self.board.possibleMoves(node):
                    if tmpBudget - cost >= 0:
                        new_lenght = z[tmpBudget-cost, nbr]+1
                        min_value = min(min_value, new_lenght)
                z[tmpBudget, node] = min_value

        return z
