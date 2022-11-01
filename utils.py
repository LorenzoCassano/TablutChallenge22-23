import numpy as np

EMPTY = 0
WHITE = 1
BLACK = 2
KING = 3

conv_to_alpha = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i' }
conv_to_matrix = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g': 6, 'h': 7, 'i': 8 }

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
    conv_to_alpha is a dict which convert the numerical column into a letter coordinate
    '''
    _from = conv_to_alpha[move[0][1] ] + str(1+ move[0][0])
    _to = conv_to_alpha[move[1][1]] + str(1 + move[1][0])
    return _from, _to

def alphanumeric_to_num(fr, to):
    '''
    return a move in the format :
    [(i, j), (x, y)]
    '''
    num_fr = conv_to_matrix[fr[0]], int(fr[1]) - 1
    num_to = conv_to_matrix[to[0]], int(to[1]) - 1 
    return (num_fr, num_to)


