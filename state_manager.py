import numpy as np
from utils import num_to_alphanumeric, BLACK

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

class State_Manager:

    def __init__(self, color, timeout, king_position = (4,4)):
        self.color = color
        self.timeout = timeout
        self.king_position = king_position

    def set_color(self, color):
        self.color = color
    def print_legal_moves(self, board):
        ''' 
        It gets all the legal moves, convert to alphanumeric and print it
        '''
        alpha_moves = []
        if self.color == 'WHITE':
            soldier_moves, king_moves = self.legalMoves(board)
            # Cycle over the soldiers
            for fr in soldier_moves:
                # Cycle over the possible moves of him
                for to in soldier_moves[fr]:
                    move = num_to_alphanumeric((fr, to))
                    alpha_moves.append(move)
            # Repeat with king
            for fr in king_moves:
                for to in king_moves[fr]:
                    move = num_to_alphanumeric((fr, to))
                    alpha_moves.append(move)

        elif self.color == 'BLACK':
            soldier_moves = self.legalMoves(board)
            # Cycle over the soldiers
            for fr in soldier_moves:
                # Cycle over the possible moves of him
                for to in soldier_moves[fr]:
                    move = num_to_alphanumeric((fr, to))
                    alpha_moves.append(move)
        print(alpha_moves)


    def legalMoves(self, board):
        '''
        legal moves are stored into dictionaries, 2 for the white player(white pawns, king pawn) and 1 for the balck player
        Legal moves white pawns:
        {(coordXPawn,coordYPawn):[(coordXLegalMove,coordYLegalMove),(),...]}
        '''
        if self.color == 'BLACK':
            return self.legal_Black_Moves(board)
        else:
            return self.legal_White_Moves(board), self.legal_King_Moves(board)
    def legal_White_Moves(self, board):

        legal_Moves = {}
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 1:
                    moves_horizontal_white = self.check_Horizontal_moves(board, (i, j))
                    moves_vertical_white = self.check_Vertical_moves(board, (i, j))
                    legal_Moves[(i,j)] = moves_horizontal_white + moves_vertical_white
        return legal_Moves
    def check_Horizontal_moves(self,board, pos):
        x = pos[0]
        y = pos[1]

        moves = []

        for i in range(y - 1, -1, -1):
            if (x, i) in BLOCKED_MOVES:
                break
            elif board[x][i] == 0:
                moves.append((x, i))
            else:
                break
        for i in range(y + 1, 9):
            if (x, i) in BLOCKED_MOVES:
                break
            elif board[x][i] == 1:
                break
            elif board[x][i] == 2:
                break
            elif board[x][i] == 3:
                break
            else:
                moves.append((x, i))
        return moves
    def check_Vertical_moves(self,board, pos):
        x = pos[0]
        y = pos[1]

        moves = []
        for i in range(x - 1, -1, -1):
            if (i, y) in BLOCKED_MOVES:
                break
            elif board[i][y] == 1:
                break
            elif board[i][y] == 2:
                break
            elif board[i][y] == 3:
                break
            else:
                moves.append((i, y))
        for i in range(x + 1, 9):
            if (i, y) in BLOCKED_MOVES:
                break
            elif board[i][y] == 1:
                break
            elif board[i][y] == 2:
                break
            elif board[i][y] == 3:
                break
            else:
                moves.append((i, y))
        return moves
    def legal_King_Moves(self, board):
        legal_Moves = {}
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 3:
                    moves_horizontal_white = self.check_Horizontal_moves((board, i, j))
                    moves_vertical_white = self.check_Vertical_moves(board, (i, j))
                    legal_Moves[(i, j)] = moves_horizontal_white + moves_vertical_white
        return legal_Moves
    def legal_Black_Moves(self, board):
        legal_Moves = {}
        
        for i in range(9):
            for j in range(0, 9):
                camp = -1                   # camp -1 == the checker is not in any camp
                moves = []
                
                if board[i, j] == 2:
                    if (i, j) in STARTING_BLACK:
                        if i//2 == 0: camp = 0
                        elif i//6 == 1: camp = 2
                        elif j//2 == 0: camp = 1
                        elif j//6 == 1: camp = 3
                
                    # double indexes ii or jj are for NEW MOVES
                    # check horizontal moves
                    for jj in range(j - 1, -1, -1):
                        if camp != -1:
                            if (i, jj) in CAMPS[camp] and board[i, jj] == 0:
                                moves.append((i, jj))
                            elif board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif board[i, jj] == 0:
                            moves.append((i, jj))
                            
                    for jj in range(j + 1, 9):
                        if camp != -1:
                            if (i, jj) in CAMPS[camp] and board[i, jj] == 0:
                                moves.append((i, jj))
                            elif board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif board[i, jj] == 0:
                            moves.append((i, jj))
                        
                    # check vertical moves
                    for ii in range(i - 1, -1, -1):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and board[ii, j] == 0:
                                moves.append((ii, j))
                            elif board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif board[ii, j] == 0:
                            moves.append((ii, j))
                    
                    for ii in range(i + 1, 9):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and board[ii, j] == 0:
                                moves.append((ii, j))
                            elif board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif board[ii, j] == 0:
                            moves.append((ii, j))
                    
                    legal_Moves[(i,j)] = moves
        return legal_Moves

    def goal_state(self, board):
        # This methods return 1 if WHITE wins, -1 if BLACK wins, otherwise 0
        # Maybe it's possible to identify other values, e.g. 0.3 when eating a pawn
        #   Check if BLACK won
        blocks = 0

        i = self.king_position[0]
        j = self.king_position[1]

        # WHITE win possible board
        # KiNG is Free
        if self.king_position in GOAL:
            return 1

        # BLACK win possible boards
        # KiNG in the Castle (4 blocks needed)
        if i == 4 and j == 4:
            if board[i + 1, j] == BLACK: blocks = blocks + 1
            if board[i - 1, j] == BLACK: blocks = blocks + 1
            if board[i, j + 1] == BLACK: blocks = blocks + 1
            if board[i, j - 1] == BLACK: blocks = blocks + 1
            if blocks == 4: return -1

        # KiNG next to the Castle (3 blocks needed)
        elif abs(i - 4) + abs(j - 4) == 1:
            if board[i + 1, j] == BLACK or (i + 1 == 4 and j == 4): blocks = blocks + 1
            if board[i - 1, j] == BLACK or (i - 1 == 4 and j == 4): blocks = blocks + 1
            if board[i, j + 1] == BLACK or (i == 4 and j + 1 == 4): blocks = blocks + 1
            if board[i, j - 1] == BLACK or (i == 4 and j - 1 == 4): blocks = blocks + 1
            if blocks == 4: return -1

        # KiNG is in another place of the map (2 blocks needed)
        else:
            if (board[i + 1, j] == BLACK or [i + 1, j] in CAMPS) and (
                    board[i - 1, j] == BLACK or [i - 1, j] in CAMPS):
                return -1
            elif (board[i, j + 1] == BLACK or [i, j + 1] in CAMPS) and (
                    board[i, j - 1] == BLACK or [i, j - 1] in CAMPS):
                return -1

        # not in a goal state
        return 0

    def make_move(self, board, move):
        pawn = board[move[0]]
        board[move[1]] = pawn
        board[move[0]] = 0

# p = Player('WHITE', 0, np.zeros((9, 9), dtype=int))
# white,king = p.legalMoves()
# print('legal moves for white :\n', white)
# print('\nlegal moves for king:\n', king)
# p.print_legal_moves()

# b = Player('BLACK', 0)
# black = b.legalMoves()
# print('legal moves for black: \n')
# for k in black:
#     print(f"{k} = {black[k]}")


