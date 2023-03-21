import board
import matplotlib.pyplot as plt

json_file = 'pekingExpressTest1.json'
json_file = 'pekingExpressTest2.json'

game = board.Board(json_file)
playerPosition = game.start_node
computerPosition = game.start_node

print(f"nodes={game.graph.nodes}")
print(f"edges={game.graph.edges}")
print(f"critical={game.critical_locations}")
print(f"start={game.start_node}")
print(f"target={game.peking}")
print(f"budget={game.budget}")

# game.visualize()
# plt.show()

game.createDPArray()
game.findShortestPath(1)

winner = False

# while not winner:
#     print("Your possibe moves: ")
#     input("Your next move: ")