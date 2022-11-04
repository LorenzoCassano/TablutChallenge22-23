'''
Main file of tablut engine, take in input IP-address, color and time.
'''

import sys
from utils import num_to_alphanumeric, alphanumeric_to_num
from communication import Connector
from player import Player
from update_state import UpdateBoard
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
    print(board)

    
    player = Player(color, timeout, board)
    # ONLY IF WE HAVE TO DO THE FIRST MOVE
    if color == "WHITE":
        

        
        # Show the legal moves
        print('Legal Moves')
        player.print_legal_moves()
        

        # Send a move
        print("Insert a move: you have to insert the from first, and the final  position")
        fr = input("Insert the starting position (corresponds to our from) ")
        to = input("Insert the final position (corresponds to our to) ")
        
        num_move = alphanumeric_to_num(fr, to)
        up_board = UpdateBoard(board, num_move)
        new_board = up_board.board_updater()
        
        print("_________________")
        
        connector.send_move((fr, to))
        board, king_position = connector.get_state()
        print("Board after move")
        
        print(board)
        print(new_board)
    # Start to play until goal is found or time finishes
    while True:
        # First, get the state from the server and convert it.
        print("Wating enemy move")
        board, king_position = connector.get_state()
        print("Current board\n", board)

        player.set_board(board)
        print('Legal Moves')
        player.print_legal_moves()

        # Trying first move
        print("Insert a move: you have to insert the from first, and the final  position")
        fr = input("Insert the starting position (corresponds to our from) ")
        to = input("Insert the final position (corresponds to our to) ")
        num_move = alphanumeric_to_num(fr, to)
        up_board = UpdateBoard(board, num_move)
        new_board = up_board.board_updater()
        print(new_board)
        print("_____________")
        connector.send_move((fr, to))
        board, king_position = connector.get_state()
        print("Board after move")
        print(board)
        print("__________")
        

       # Then, start the search for the best move

       # algorithm computes move --> [(i,j),(x,y)]
       # convertion in a string tuple [(from, to)]
       # sending move

       # Convert the move into alphanumerical value

       # Send the move
       #pass


main()

       
       

