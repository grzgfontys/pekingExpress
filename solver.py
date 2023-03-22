from board import Board
import sys


class Solver:

    def __init__(self, board: Board):
        self.board = board
        # init Z table
        self.__z = self.__create_z()

    def z(self, a, t: int) -> int:
        """minimum distance of getting from node a to the target within cost t"""
        return self.__z[t, a]

    def shortest_paths(self, a, t: int):
        """set of the shortest paths from node a to the target within a budget t"""
        current_distance = self.z(a, t)
        if a == self.board.peking:
            yield [a]
            return

        if current_distance >= sys.maxsize or t <= 0:
            return

        for b in self.viable_moves(a, t):
            new_budget = t - self.board.cost(a, b)
            for p in self.shortest_paths(b, new_budget):
                yield [a] + p

    def blocking_cmp(self, a, b):
        """ compares paths a and b with regard to blocking
        returns 0 if there are no blocks, positive value if a blocks b, and negative value if b blocks a """
        critical_locations = self.board.critical_locations
        for i in range(len(a)):
            if a[i] in critical_locations:
                if a[i] == b[i]:
                    return 1
                elif i > 0 and a[i] == b[i - 1]:
                    return -1
        return 0

    def blocking_scores(self, a, b_paths):
        """returns a pair x,y where x is the number of paths a blocks, and y is the number of paths that block a"""
        blocking, blocked = 0, 0
        for p in b_paths:
            cmp = self.blocking_cmp(a, p)
            if cmp > 0:
                blocking += 1
            elif cmp < 0:
                blocked += 1
        return blocking, blocked

    def viable_moves(self, a, t: int):
        for b in self.board.graph.adj[a]:
            current_distance = self.z(a, t)
            cost = self.board.graph.edges[a, b]['cost']
            if t < cost:  # cannot afford
                continue
            new_distance = self.z(b, t - cost)
            if new_distance < current_distance:
                yield b

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
