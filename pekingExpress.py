import board
import solver
import matplotlib.pyplot as plt

json_file = 'pekingExpressTest1.json'
# json_file = 'pekingExpressTest2.json'



winner = False
who_starts = input("Does the player start? y/n")
# who_starts = 'y'
while who_starts != 'y' and who_starts != 'n':
    print("This is not correct answer!")
    who_starts = input("Does the player start? y/n")
if who_starts == 'y':
    board = board.Board(json_file, True)
    solver = solver.Solver(board)
else:
    board = board.Board(json_file, False)
    solver = solver.Solver(board)
    board.update_computer_pos(solver.choose_next_move_defensive())




# print(f"nodes={board.graph.nodes}")
# print(f"edges={board.graph.edges}")
# print(f"critical={board.critical_locations}")
# print(f"start={board.start_node}")
# print(f"target={board.peking}")
# print(f"budget={board.budget}")

# board.visualize()
# plt.show()

while not winner:
    print(f"Computer position { board.computer_pos } and budget { board.computer_budget }")
    print(f"Your position { board.player_pos } and budget { board.player_budget }")

    # Player wins
    if board.player_pos == 88 and board.computer_pos == 88:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~ Tie! ~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    elif board.player_already_at_88 == 2:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~ You have won! ~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    elif board.computer_already_at_88 == 2:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~ You have lost! ~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    # If player does not win and has no budget then he loses
    elif board.player_budget <= 0:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~ You do not have money! ~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        break
    # If player does not win or lose he still playes 
    else:
        print("Your possibe moves: ")
        print("---")

        possible_moves = board.possibleMovesPlayer()
        for nbr in possible_moves.keys():
            print(f"- Move to { nbr } with cost of { possible_moves[nbr] }")
        print("- Type '0' to stay in place")

        print("---")

        try:
            next_move = int(input("Your next move: "))
        except:
            next_move = None

        while next_move not in possible_moves.keys() and next_move != 0:
            print("This is not correct move!")
            try:
                next_move = int(input("Your next move: "))
            except:
                continue
        if next_move != 0:
            board.player_pos = next_move
            board.player_budget -= possible_moves[next_move]
        if board.player_pos == 88:
            board.player_already_at_88 += 1
        print("~~~~~~")
        board.update_computer_pos(solver.choose_next_move_defensive())
        if board.computer_pos == 88:
            board.computer_already_at_88 += 1
