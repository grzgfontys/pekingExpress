import board
import solver
import matplotlib.pyplot as plt
from solver import Solver

json_file = 'pekingExpressTest1.json'
# json_file = 'pekingExpressTest2.json'

board = board.Board(json_file)
playerPosition = board.start_node
computerPosition = board.start_node

print(f"nodes={board.graph.nodes}")
print(f"edges={board.graph.edges}")
print(f"critical={board.critical_locations}")
print(f"start={board.start_node}")
print(f"target={board.peking}")
print(f"budget={board.budget}")

# board.visualize()
# plt.show()

solver = solver.Solver(board)


winner = False


print([p for p in solver.shortest_paths(1, 3)])

# while not winner:
#     print("Your possibe moves: ")
#     input("Your next move: ")