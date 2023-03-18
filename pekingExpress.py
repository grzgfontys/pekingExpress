import board
import matplotlib.pyplot as plt

json_file = 'pekingExpressTest1.json'

game = board.Board(json_file)

print(f"nodes={game.graph.nodes}")
print(f"edges={game.graph.edges}")
print(f"critical={game.critical_locations}")
print(f"start={game.start_node}")
print(f"target={game.target_node}")
print(f"budget={game.budget}")

game.visualize()
plt.show()
