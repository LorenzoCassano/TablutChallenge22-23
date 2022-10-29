import numpy as np

BLOCKED_MOVES_WHITE_PLAYER = \
    ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4), (4, 7), (3, 8),
     (4, 8),
     (5, 8))

BLACK = (
    (0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4), (4, 7), (3, 8),
    (4, 8),
    (5, 8))
WHITE = ((4, 2), (4, 3), (4, 5), (4, 6), (2, 4), (3, 4), (5, 4), (6, 4))





class Player:

    def __init__(self, color, timeout, board):
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

    '''
    legal moves are stored into dictionaries, 2 for the white player(white pawns, king pawn) and 1 for the balck player
    Legal moves white pawns:
      {(coordXPawn,coordYPawn):[(coordXLegalMove,coordYLegalMove),(),...]}
    '''
    def legalMoves(self):
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
            if (x, i) in BLOCKED_MOVES_WHITE_PLAYER:
                break
            elif self.board[x][i] == 1:
                break
            elif self.board[x][i] == 2:
                break
            elif self.board[x][i] == 3:
                break
            else:
                moves.append((x, i))
        for i in range(y + 1, 9):
            if (x, i) in BLOCKED_MOVES_WHITE_PLAYER:
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
            if (i, y) in BLOCKED_MOVES_WHITE_PLAYER:
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
            if (i, y) in BLOCKED_MOVES_WHITE_PLAYER:
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
        pass


p = Player('WHITE', 0, np.zeros((9, 9)))
white,king = p.legalMoves()
print('legal moves for white :\n', white)
print('\nlegal moves for king:\n', king)
