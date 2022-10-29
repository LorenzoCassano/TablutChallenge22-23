'''
Main file of tablut engine, take in input IP-address, color and time.
'''

#import sys
from utils import num_to_alphanumeric
from communication import Connector

def main():
    #color = sys.args[1]
    #timeout = sys.args[2]

    name = "Mbappe"
    color = "BLACK" #sys.argv[1]
    timeout = int(100)#int(sys.argv[2])
    print("Hi, i'm " + name + ", I will play as " + color + " and I have " + str(timeout))
    # if arg is null localhost is chosen
    #if len(sys.argv) == 4:
     #   server_address = sys.argv[3]
    #else:
    server_address = 'localhost'
    print("\nConnection to: " + server_address)

    connector = Connector(name, color, server_address)
    connector.connection()
    #tp = TablutPlayer(color, timeout, board)
    print("\nInitial state:")
    # tp.display(state)
    board, king_position = connector.get_state()

    print(board)

    #old_board = copy.deepcopy(board)
    i = 0
    # Who sents the first move ? --> Testing with server

    # 1) Retrieve the server address if not  local
    
    # 2) Connect to the server 

    # 3) Initialize the player

    # 4) Start to play until goal is found or time finishes
    while True:
        board, king_position = connector.get_state()
        # Trying first move
        connector.send_move(("D9", "C9"))
        print(board)
        if True:
            break
       #First, get the state from the server and convert it.

       # Then, start the search for the best move

       

       # algorithm computes move --> [(i,j),(x,y)]
       # convertion in a string tuple [(from, to)]
       # sending move



       # Convert the move into alphanumerical value

       # Send the move
       #pass



if __name__ == "__main__":
    main()

       
       

