'''
Main file of tablut engine, take in input IP-address, color and time.
'''

import sys
from utils import num_to_alphanumeric, alphanumeric_to_num
from communication import Connector
from state_manager import State_Manager
from aima.games import *
from engine.game import TablutGame

def help():
    print("This is the MbAppe Algorithm which is able to play to Tablut\n")
    print("To play is necessary to run Tablut Server and to use the following parameters:")
    print("-color must be 'WHITE' or 'BLACK'\n-timeout\n-server address is optional, default value is 'localhost'")


def main():
    # Checking principal arguments
    try:
        color = sys.argv[1]
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            help()
            return
        timeout = int(sys.argv[2])
    except Exception:
        print("Not argument given")
        return

    if color != "WHITE" and color != "BLACK":
        print("The color must be WHITE or BLACK")
        return

    # starting the connection
    name = "Mbappe"
    print("Hi, i'm " + name + ", I will play as " + color + " and I have " + str(timeout))

    if len(sys.argv) == 4:
        server_address = sys.argv[3]
    else:
        server_address = 'localhost'

    print("\nConnection to: " + server_address)
    connector = Connector(name, color, server_address)
    connector.connection()

    # Starting game
    print("Initial state:")
    board, king_position = connector.get_state()
    print("Initial board")
    print(board)

    player = TablutGame(color, board, king_position)
    # ONLY IF WE HAVE TO DO THE FIRST MOVE

    # Start to play until goal is found or time finishes
    if color == "BLACK":

        # White player has to do the first mo ve
        board, king_position = connector.get_state()
        print("Board after enemy moves")
        print(board)

    while True:
      # First, get the state from the server and convert it.
        
        state = GameState(to_move=color,
                          utility= player.manager.heuristics(board),
                          board= board,
                         moves= player.manager.legalMoves(board))

        # Trying first move
        time_left = timeout
        
        # for depth in range(1, 5):
        for depth in range(1, 4):
            actual_move, time_cost, exit = alpha_beta_cutoff_search(state, player, time_left, depth)
            if exit:
                break
            else:
                time_left -= time_cost
                move = actual_move
            if time_left < 15:
                break
        
        # print("La mossa vale ",move)
        move = num_to_alphanumeric(move)
        print("Move choice ",move)
        print("Time to compute the move ",round(time_cost,2))
        connector.send_move(move)
        try:
            board, king_position = connector.get_state()
            print("Board after move")
            print(board)
            print("BLACK SOLDIERS = {}\nWHITE PAWNS = {}".format(np.sum(board == 2), np.sum(board == 1) + 1))
            print("Waiting for enemy move....")
            board, king_position = connector.get_state()
            print("Enemy move:")
            print(board)
        except Exception:
            print("Game Finished")
            return
        
    # Then, start the search for the best move

    # algorithm computes move --> [(i,j),(x,y)]
    # convertion in a string tuple [(from, to)]
    # sending move

    # Convert the move into alphanumerical value

    # Send the move
    # pass


main()
