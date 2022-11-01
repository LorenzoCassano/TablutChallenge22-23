import numpy as np
from utils import num_to_alphanumeric

BLOCKED_MOVES = \
    ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4), (4, 7), (3, 8), (4, 8), (5, 8),
     (4, 4))

BLACK = ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4), (4, 7), (3, 8), (4, 8), (5, 8))
WHITE = ((4, 2), (4, 3), (4, 5), (4, 6), (2, 4), (3, 4), (5, 4), (6, 4))

CAMPS = (((0, 3), (0, 4), (0, 5), (1, 4)), 
         ((3, 0), (4, 0), (5, 0), (4, 1)),
         ((8, 3), (8, 4), (8, 5), (7, 4)),
         ((4, 7), (3, 8), (4, 8), (5, 8)))



class Player:

    def __init__(self, color, timeout, board = np.zeros((9, 9), dtype=int)):
        self.color = color
        self.timeout = timeout
        self.board = board
        for i in range(0, 9):
            for j in range(0, 9):
                if (i, j) in BLACK:
                    self.board[i][j] = 2
                elif (i, j) in WHITE:
                    self.board[i][j] = 1
                elif i == j == 4:
                    self.board[i][j] = 3
                else:
                    self.board[i][j] = 0
        print(self.board)

    def set_board(self, board):
        ''' 
        Update the board state
        '''
        self.board = board
    
    def print_legal_moves(self):
        ''' 
        It gets all the legal moves, convert to alphanumeric and print it
        '''
        alpha_moves = []
        if self.color == 'WHITE':
            soldier_moves, king_moves = self.legalMoves()
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
            soldier_moves = self.legalMoves()
            # Cycle over the soldiers
            for fr in soldier_moves:
                # Cycle over the possible moves of him
                for to in soldier_moves[fr]:
                    move = num_to_alphanumeric((fr, to))
                    alpha_moves.append(move)
        print(alpha_moves)
                    
                

    def legalMoves(self):
        '''
        legal moves are stored into dictionaries, 2 for the white player(white pawns, king pawn) and 1 for the balck player
        Legal moves white pawns:
        {(coordXPawn,coordYPawn):[(coordXLegalMove,coordYLegalMove),(),...]}
        '''
        if self.color == 'BLACK':
            return self.legal_Black_Moves()
        else:
            return self.legal_White_Moves(), self.legal_King_Moves()
    def legal_White_Moves(self):

        legal_Moves = {}
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 1:
                    moves_horizontal_white = self.check_Horizontal_moves((i, j))
                    moves_vertical_white = self.check_Vertical_moves((i, j))
                    legal_Moves[(i,j)] = moves_horizontal_white + moves_vertical_white
        return legal_Moves
    def check_Horizontal_moves(self,pos):
        x = pos[0]
        y = pos[1]

        moves = []

        for i in range(y - 1, -1, -1):
            if (x, i) in BLOCKED_MOVES:
                break
            elif self.board[x][i] == 0:
                moves.append((x, i))
            else:
                break
        for i in range(y + 1, 9):
            if (x, i) in BLOCKED_MOVES:
                break
            elif self.board[x][i] == 1:
                break
            elif self.board[x][i] == 2:
                break
            elif self.board[x][i] == 3:
                break
            else:
                moves.append((x, i))
        return moves
    def check_Vertical_moves(self, pos):
        x = pos[0]
        y = pos[1]

        moves = []
        for i in range(x - 1, -1, -1):
            if (i, y) in BLOCKED_MOVES:
                break
            elif self.board[i][y] == 1:
                break
            elif self.board[i][y] == 2:
                break
            elif self.board[i][y] == 3:
                break
            else:
                moves.append((i, y))
        for i in range(x + 1, 9):
            if (i, y) in BLOCKED_MOVES:
                break
            elif self.board[i][y] == 1:
                break
            elif self.board[i][y] == 2:
                break
            elif self.board[i][y] == 3:
                break
            else:
                moves.append((i, y))
        return moves

    def legal_King_Moves(self):
        legal_Moves = {}
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 3:
                    moves_horizontal_white = self.check_Horizontal_moves((i, j))
                    moves_vertical_white = self.check_Vertical_moves((i, j))
                    legal_Moves[(i, j)] = moves_horizontal_white + moves_vertical_white
        return legal_Moves
    
    def legal_Black_Moves(self):
        legal_Moves = {}
        
        for i in range(9):
            for j in range(0, 9):
                camp = -1                   # camp -1 == the checker is not in any camp
                moves = []
                
                if self.board[i, j] == 2:
                    if (i, j) in BLACK:
                        if i//2 == 0: camp = 0
                        elif i//6 == 1: camp = 2
                        elif j//2 == 0: camp = 1
                        elif j//6 == 1: camp = 3
                
                    # double indexes ii or jj are for NEW MOVES
                    # check horizontal moves
                    for jj in range(j - 1, -1, -1):
                        if camp != -1:
                            if (i, jj) in CAMPS[camp] and self.board[i, jj] == 0:
                                moves.append((i, jj))
                            elif self.board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif self.board[i, jj] == 0:
                            moves.append((i, jj))
                            
                    for jj in range(j + 1, 9):
                        if camp != -1:
                            if (i, jj) in CAMPS[camp] and self.board[i, jj] == 0:
                                moves.append((i, jj))
                            elif self.board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif self.board[i, jj] == 0:
                            moves.append((i, jj))
                        
                    # check vertical moves
                    for ii in range(i - 1, -1, -1):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and self.board[ii, j] == 0:
                                moves.append((ii, j))
                            elif self.board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif self.board[ii, j] == 0:
                            moves.append((ii, j))
                    
                    for ii in range(i + 1, 9):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and self.board[ii, j] == 0:
                                moves.append((ii, j))
                            elif self.board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif self.board[ii, j] == 0:
                            moves.append((ii, j))
                    
                    legal_Moves[(i,j)] = moves
        return legal_Moves        
                
                    
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


