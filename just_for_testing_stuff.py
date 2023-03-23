import sys

from board import Board
from solver import Solver

json_file = 'pekingExpressTest3.json'

pos_a = 1
budget_a = 6
pos_b = 5
budget_b = 5
a_is_white = True

board = Board(json_file, not a_is_white)
board.computer_pos = pos_a
board.computer_budget = budget_a
board.player_pos = pos_b
board.player_budget = budget_b
solver = Solver(board)

viable_moves_a = solver.viable_moves(pos_a, budget_a)
viable_moves_a = [*viable_moves_a]
print(f"{viable_moves_a=}")

evaluation, move = solver.minimax(pos_a, budget_a, pos_b, budget_b, a_is_white, -sys.maxsize, sys.maxsize,
                                  depth=sys.maxsize, playing_a=True)
print(f"{evaluation=}, {move=}")

print("===== END MINIMAX =====")

paths_a = list(solver.shortest_paths(pos_a, budget_a))
paths_b = list(solver.shortest_paths(pos_b, budget_b))

print(f"Paths A:")
for p in paths_a:
    x, y = solver.blocking_scores(p, paths_b)
    print(f"{p} ({y},{x})")

print(f"Paths B:")
for p in paths_b:
    print(f"{p}")

move_2 = solver.choose_next_move_defensive()

print(f"{move_2=}")
