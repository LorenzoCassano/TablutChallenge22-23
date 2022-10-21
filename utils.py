import numpy as np

EMPTY = 0
WHITE = 1
BLACK = 2
KING = 3

conv = { 0 :'a', 1 : 'b', 2 : 'c', 3 : 'd', 4 : 'e', 5 : 'f', 6 : 'g', 7 : 'h', 8 : 'i' }

def converter(json_state):
    '''
    Input : json object with info on the state
    Returns : 
    '''
    # Convert to list
    data = list(json_state.items())
    # Convert to array
    ar = np.array(data, dtype = object)
    # Selecting board (the array is (2,2) matrix, it has board and turn info)
    board_array = np.array(ar[0,1], dtype=object)   
    # Converting in a numerical matrix
    board_state = np.zeros((9,9))
    for i in range(0,9):
        for j in range (0,9):
            if board_array[i,j] == 'EMPTY':
                board_state[i,j] = EMPTY
            elif board_array[i,j] == 'WHITE':
                board_state[i,j] = WHITE
            elif board_array[i,j] == 'BLACK':
                board_state[i,j] = BLACK
            elif board_array[i,j] == 'KING':
                board_state[i,j] = KING
                king_position = (i,j)

    return board_state, king_position

def num_to_alphanumeric(move):
    '''
    move = [(i,j),(x,y)]
    conv is a dict which convert the numerical column into a letter coordinate
    '''
    _from = conv[move[0][1] ] + str(1+ move[0][0])
    _to = conv[move[1][1]] + str(1 + move[1][0])
    return _from, _to


