import board
import solver
import matplotlib.pyplot as plt

json_file = 'pekingExpressTest1.json'
# json_file = 'pekingExpressTest2.json'

board = board.Board(json_file)

# print(f"nodes={board.graph.nodes}")
# print(f"edges={board.graph.edges}")
# print(f"critical={board.critical_locations}")
# print(f"start={board.start_node}")
# print(f"target={board.peking}")
# print(f"budget={board.budget}")

# board.visualize()
# plt.show()

solver = solver.Solver(board)


winner = False


print([p for p in solver.shortest_paths(1, 3)])

while not winner:
    print(f"Your position { board.player_pos } and budget { board.player_budget }")

    # Player wins
    if board.player_pos == 88:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~ You have won! ~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    # If player does not win and has no budget then he loses
    elif board.player_budget <= 0:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~ You have lost! ~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    # If player does not win or lose he still playes 
    else:
        print("Your possibe moves: ")
        print("---")

        possible_moves = board.possibleMovesPlayer()
        for nbr in possible_moves.keys():
            print(f"- Move to { nbr } with cost of { possible_moves[nbr] }")

        print("---")

        next_move = int(input("Your next move: "))
        board.player_pos = next_move
        board.player_budget -= possible_moves[next_move]
        print("~~~~~~")
