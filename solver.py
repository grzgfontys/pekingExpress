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

        # not necessary, but break early
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
            cost = self.board.cost(a, b)
            if t < cost:  # cannot afford
                continue
            new_distance = self.z(b, t - cost)
            if new_distance < current_distance:
                yield b

    def defensive_strategy(self, a_paths, b_paths):
        """chooses the path from a that minimizes chance of getting blocked by b and maximizes chances of blocking b"""
        b_paths = list(b_paths)  # convert to list to prevent multiple enumerations of a generator
        blocking_min, blocked_max, best_path = sys.maxsize, 0, None
        for a in a_paths:
            blocking, blocked = self.blocking_scores(a, b_paths)
            if blocking < blocking_min or (blocking == blocking_min and blocked > blocked_max):
                blocking_min, blocked_max, best_path = blocking, blocked, a

        assert best_path is not None
        return best_path

    def choose_next_move_defensive(self, pos_a, budget_a, pos_b, budget_b):
        a_paths = self.shortest_paths(pos_a, budget_a)
        b_paths = self.shortest_paths(pos_b, budget_b)
        best_path = self.defensive_strategy(a_paths, b_paths)

        # the first is pos_a, so we return the second node
        return best_path[1]

    def __create_z(self):
        z = dict()

        for budget in range(self.board.budget + 1):
            for node in self.board.graph.nodes():
                if node == self.board.peking:
                    z[budget, node] = 0
                    continue
                min_length = sys.maxsize
                for nbr, cost in self.board.possibleMoves(node):
                    if budget - cost >= 0:
                        new_length = z[budget - cost, nbr] + 1
                        min_length = min(min_length, new_length)
                z[budget, node] = min_length

        return z
