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
        blocking, blocked_by = 0, 0
        for p in b_paths:
            cmp = self.blocking_cmp(a, p)
            if cmp > 0:
                blocking += 1
            elif cmp < 0:
                blocked_by += 1
        return blocking, blocked_by

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
        b_paths = list(
            b_paths)  # convert to list to prevent multiple enumerations of a generator
        blocked_min, blocking_max, best_path = sys.maxsize, 0, None
        for a in a_paths:
            blocking, blocked = self.blocking_scores(a, b_paths)
            if blocked < blocked_min or (blocked == blocked_min and blocking > blocking_max):
                blocked_min, blocking_max, best_path = blocked, blocking, a

        assert best_path is not None
        return best_path

    def choose_next_move_defensive(self):
        pos_b = self.board.player_pos
        budget_b = self.board.computer_budget
        pos_a = self.board.computer_pos
        budget_a = self.board.player_budget

        a_paths = self.shortest_paths(pos_a, budget_a)
        available_a_paths = (
            p for p in a_paths if p[1] != pos_b or p[1] not in self.board.critical_locations)
        b_paths = self.shortest_paths(pos_b, budget_b)
        best_path = self.defensive_strategy(a_paths, b_paths)

        # the first is pos_a, so we return the second node
        return best_path[1]

    def __game_over_score(self, pos_a, budget_a, pos_b, budget_b, a_is_white):
        target = self.board.peking
        if pos_a != target and pos_b != target:
            return None
        if pos_b == target and pos_a == target:
            raise "Should not happen"  # should be evaluated earlier
        if a_is_white:
            if pos_b == target:
                return -sys.maxsize  # black win
            if pos_a == target:
                if target in self.viable_moves(pos_b, budget_b):
                    return 0  # b can reach target just after white, tie
                else:
                    return sys.maxsize  # white wins
        else:  # b is white
            if pos_a == target:
                return sys.maxsize  # black win
            if pos_b == target:
                if target in self.viable_moves(pos_a, budget_a):
                    return 0  # a can reach target just after white, tie
                else:
                    return -sys.maxsize  # white wins

    def minimax(self, pos_a, budget_a, pos_b, budget_b, a_is_white, depth, playing_a):
        static_eval = self.__game_over_score(
            pos_a, budget_a, pos_b, budget_b, a_is_white)
        if static_eval is not None:
            return static_eval, (pos_a if playing_a else pos_b)
        if depth == 0:
            # heuristic
            return (self.z(pos_b, budget_b) - self.z(pos_a, budget_a)), (pos_a if playing_a else pos_b)
        if playing_a:  # maximizing
            max_score, best_move = -sys.maxsize, None
            for next_pos in self.viable_moves(pos_a, budget_a):
                if next_pos in self.board.critical_locations and next_pos == pos_b:
                    continue  # not viable after all
                new_budget = budget_a - self.board.cost(pos_a, next_pos)
                score, _ = self.minimax(
                    next_pos, new_budget, pos_b, budget_b, a_is_white, depth - 1, False)
                if score > max_score:
                    max_score = score
                    best_move = next_pos
            return max_score, best_move
        else:  # minimizing
            min_score, best_move = sys.maxsize, None
            for next_pos in self.viable_moves(pos_b, budget_b):
                if next_pos in self.board.critical_locations and next_pos == pos_a:
                    continue  # not viable after all
                new_budget = budget_b - self.board.cost(pos_b, next_pos)
                score, _ = self.minimax(
                    pos_a, budget_a, next_pos, new_budget, a_is_white, depth - 1, True)
                if score < min_score:
                    min_score = score
                    best_move = next_pos
            return min_score, best_move

    def __create_z(self):
        z = dict()

        for budget in range(self.board.starting_budget + 1):
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
