import numpy as np

conv_to_alpha = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i' }
conv_to_matrix = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f':5, 'g': 6, 'h': 7, 'i': 8 }

"""
For handling the board
"""

EMPTY = 0
WHITE = 1
BLACK = 2
KING = 3

BL_MOVES = (
    (0, 0, 0, 1, 3, 4, 5, 4, 8, 8, 8, 7, 4, 3, 4, 5, 4),
    (3, 4, 5, 4, 0, 0, 0, 1, 3, 4, 5, 4, 7 ,8, 8, 8, 4)
)

#board_array = np.zeros((9, 9), dtype=np.int8)
block_arr = np.zeros((9, 9), dtype=np.int8)
block_arr[BL_MOVES] = 1

moves_arr = np.zeros((9, 9), dtype=np.int8)


BLOCKED_MOVES = ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4),
                 (4, 7), (3, 8), (4, 8), (5, 8), (4, 4))

STARTING_BLACK = ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4), (4, 7),
                  (3, 8), (4, 8), (5, 8))

STARTING_WHITE = ((4, 2), (4, 3), (4, 5), (4, 6), (2, 4), (3, 4), (5, 4), (6, 4))

CAMPS = (((0, 3), (0, 4), (0, 5), (1, 4)),
         ((3, 0), (4, 0), (5, 0), (4, 1)),
         ((8, 3), (8, 4), (8, 5), (7, 4)),
         ((4, 7), (3, 8), (4, 8), (5, 8)))

GOAL = ((0, 1), (0, 2), (0, 6), (0, 7),
        (8, 1), (8, 2), (8, 6), (8, 7),
        (1, 0), (2, 0), (6, 0),(7, 0),
        (1,8), (2, 8), (6, 8), (7,8))

CASTLE = (4, 4)

CASTLE_NEIGHBOUR = ((4, 3), (4, 5), (3, 4), (5, 4))

KING_PROMISING = ((2, 2), (2, 3), (3, 2),
            (3, 3), (2, 5), (2, 6),
            (3, 5), (3, 6), (5, 2),
            (5, 3), (6, 2), (6, 3),
            (5, 5), (5, 6), (6, 5),
            (6, 6))

SPECIAL_BOXES = ((2, 3), (3, 2), (2, 5), (3, 6), (6, 3), (5, 2), (5, 6), (6, 5))

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


