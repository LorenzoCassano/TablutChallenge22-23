import numpy as np
from utils import *
import copy

class State_Manager:

    def __init__(self, color, king_position = (4,4)):
        self.color = color
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
            return self.legal_White_Moves(board) + self.legal_King_Moves(board)

    def legal_White_Moves(self, board):

        legal_Moves = []
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i,j] == WHITE:
                    moves_horizontal_white = self.check_Horizontal_moves(board, (i, j))
                    moves_vertical_white = self.check_Vertical_moves(board, (i, j))
                    legal_Moves += moves_horizontal_white + moves_vertical_white

        return legal_Moves

    def check_Horizontal_moves(self,board, pos):
        x = pos[0]
        y = pos[1]

        moves = []

        for i in range(y - 1, -1, -1):
            if (x, i) in BLOCKED_MOVES:
                break
            elif board[x][i] == 0:
                moves.append( ( (x,y),(x,i) ) )
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
                moves.append( ( (x,y),(x,i) ) )
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
                moves.append( ( (x,y),(i,y) ) )
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
                moves.append( ( (x,y),(i,y) ) )
        return moves

    def legal_King_Moves(self, board):
        legal_Moves = []
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 3:
                    moves_horizontal_white = self.check_Horizontal_moves(board,(i, j))
                    moves_vertical_white = self.check_Vertical_moves(board, (i, j))
                    legal_Moves += moves_horizontal_white + moves_vertical_white
        return legal_Moves

    def legal_Black_Moves(self, board):
        legal_Moves = []
        
        for i in range(9):
            for j in range(0, 9):
                camp = -1                   # camp -1 == the checker is not in any camp
                if board[i, j] == BLACK:
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
                                legal_Moves.append( ((i,j),(i, jj)) )
                            elif board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif board[i, jj] == 0:
                            legal_Moves.append(((i, j), (i, jj)))
                            
                    for jj in range(j + 1, 9):
                        if camp != -1:
                            if (i, jj) in CAMPS[camp] and board[i, jj] == 0:
                                legal_Moves.append(((i, j), (i, jj)))
                            elif board[i, jj] != 0:
                                break
                            
                        if (i, jj) in BLOCKED_MOVES:
                            break
                        elif board[i, jj] == 0:
                            legal_Moves.append( ((i, j), (i, jj)) )
                        
                    # check vertical moves
                    for ii in range(i - 1, -1, -1):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and board[ii, j] == 0:
                                legal_Moves.append(((i, j), (ii, j)))
                            elif board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif board[ii, j] == 0:
                            legal_Moves.append(((i, j), (ii, j)))
                    
                    for ii in range(i + 1, 9):
                        if camp != -1:
                            if (ii, j) in CAMPS[camp] and board[ii, j] == 0:
                                legal_Moves.append(((i, j), (ii, j)))
                            elif board[ii, j] != 0:
                                break
                            
                        if (ii, j) in BLOCKED_MOVES:
                            break
                        elif board[ii, j] == 0:
                            legal_Moves.append(((i, j), (ii, j)))

        return legal_Moves

    def boxscore(self, i, j):
        if (i, j) in STARTING_BLACK:
            return 0.012
        elif (i, j) == (4, 4):
            return 0.02
        elif (i, j) in SPECIAL_BOXES:
            return 0.015
        else:
            return 0.01

    def heuristics(self, board):
        """
        This function returns a value in the domain [-1, 1] where 1 is for the victory of white (MAX player) and -1 for the victory of black (MIN player).
        This score is calculated basing on how many checkers are still in the board, and which boxes do they occupy. A different value is assigned to different boxes, basing on the coontrol power that box has on the board.
        This value is then added to the score if that box is occupied by WHITE, and subtracted if that box is occupied by BLACK.

        score = 0
        for i in range(9):
            for j in range(9):
                if board[i, j] in (WHITE, KING):
                    score += self.boxscore(i, j)
                elif board[i, j] == BLACK:
                    score -= self.boxscore(i, j)
        return score

        """
        white_count = 0
        black_count = 0
        score = 0
        for i in range(9):
            for j in range(9):
                if board[i, j] == WHITE:
                    white_count += 1
                elif board[i, j] == BLACK:
                    black_count += 1
        if self.king_position in CASTLE_NEIGHBOUR:
            score = 0.2
            ### Only if king not in danger (black soldiers near to him (1, 2)) 
        elif self.king_position in KING_PROMISING:
            score = 0.4
            ### Only if king not in danger ()
        score += (white_count - black_count) / (white_count + black_count)    
        return score

    def utility_state(self, board):
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
        #return self.heuristics(board)
        return np.random.rand(1)


    def finding_coord(self, board, dest_move):
        '''
        return attributes up, down, right, left if are in the board
        '''
        coord_to_check = {}
        if dest_move[0] != 0:
            coord_to_check["UP"] = (dest_move[0] - 1, dest_move[1])
        if dest_move[0] != 8:
            coord_to_check["DOWN"] = (dest_move[0] + 1, dest_move[1])
        if dest_move[1] != 0:
            coord_to_check["LEFT"] = (dest_move[0], dest_move[1] - 1)
        if dest_move[1] != 8:
            coord_to_check["RIGHT"] = (dest_move[0], dest_move[1] + 1)
        return coord_to_check

    def check_near_enemies(self,board, dest_move):
        '''
        return a list of tuples with the coord of the opponent soldiers that could be taken out (the one near it)
        (it could be empty)
        '''
        enemies = []
        coord_to_check = self.finding_coord(board, dest_move)
        if self.color == WHITE:
            for key in coord_to_check:
                if board[coord_to_check[key][0], coord_to_check[key][1]] == BLACK:
                    enemies.append(coord_to_check[key])
        else:
            for key in coord_to_check:
                if board[coord_to_check[key][0], coord_to_check[key][1]] == WHITE or \
                        board[coord_to_check[key][0], coord_to_check[key][1]] == KING:
                    enemies.append(coord_to_check[key])
        return enemies

    def get_direction(self, enemy_spot, dest_move):
        x_en, y_en = enemy_spot
        x_al, y_al = dest_move
        if x_en == x_al:
            if y_en == y_al + 1:
                direction = 'RIGHT'
            else:
                direction = 'LEFT'
        else:
            # Same Y
            if x_en == x_al + 1:
                direction = "UP"
            else:
                direction = 'DOWN'
        return direction

    def board_updater(self, board, move):
        '''
        return the new state generated by the move
        '''
        start_move = move[0]
        dest_move = move[1]
        new_board = copy.deepcopy(board)
        win = None
        
        if new_board[start_move[0], start_move[1]] == KING:
            self.king_position = dest_move
            new_board[dest_move[0], dest_move[1]] = KING
            if dest_move in GOAL:
                win = 1 # White win
        else:
            new_board[dest_move[0], dest_move[1]] = (WHITE if self.color == "WHITE" else BLACK)
        # Get the near enemies
        new_board[start_move[0], start_move[1]] = EMPTY
        enemies = self.check_near_enemies(board, dest_move)
        if len(enemies) != 0:
            for enemy_spot in enemies:
                if self.take(board, enemy_spot, dest_move) == KING:
                    win = -1
                if self.take(board,enemy_spot, dest_move) == True:
                    new_board[enemy_spot[0], enemy_spot[1]] = EMPTY
        return new_board, win

    def take(self, board, enemy_spot, dest_move):
        '''
        Check if the near enemy has to be taken out
        '''
        x = enemy_spot[0]
        y = enemy_spot[1]

        # FIRST CASE : the opponent which is attacked is the king
        if board[x, y] == KING:
            # Check its postition
            if (x, y) == CASTLE:
                if board[x + 1, y] == BLACK and \
                        board[x - 1, y] == BLACK and \
                        board[x, y + 1] == BLACK and \
                        board[x, y - 1] == BLACK:
                    return KING

            elif (x, y) in CASTLE_NEIGHBOUR:
                neighbours_count = 0
                for coords in CASTLE_NEIGHBOUR:
                    if board[coords[1], coords[0]] == BLACK:
                        neighbours_count += 1
                if neighbours_count >= 3:
                    return KING
            else:
                # KING isn't in the castle or in its neighbourhood
                # He is taken out as a simple soldier
                direction = self.get_direction(enemy_spot, dest_move)
                if direction == "UP" and x - 1 >= 0:
                    if board[x - 1, y] == BLACK or \
                            (x - 1, y) in CAMPS or \
                            (x - 1, y) == CASTLE:
                        return KING
                if direction == "DOWN" and x + 1 <= 8:
                    if board[x + 1, y] == BLACK or \
                            (x + 1, y) in CAMPS or \
                            (x + 1, y) == CASTLE:
                        return True
                if direction == "LEFT" and y - 1 >= 0:
                    if board[x, y - 1] == BLACK or \
                            (x, y - 1) in CAMPS or \
                            (x, y - 1) == CASTLE:
                        return True
                elif y + 1 <= 8:
                    if board[x, y + 1] == BLACK or \
                            (x, y + 1) in CAMPS or \
                            (x, y + 1) == CASTLE:
                        take_out = True
        # SECOND CASE : the opponent which is attacked is a black soldier
        elif board[enemy_spot[0], enemy_spot[1]] == BLACK:
            if (x, y) not in CAMPS:
                direction = self.get_direction(enemy_spot,dest_move)
                if direction == "UP" and x - 1 >= 0:
                    if board[x - 1, y] == WHITE or \
                            (x - 1, y) in CAMPS or \
                            (x - 1, y) == CASTLE:
                        return True
                if direction == "DOWN" and x + 1 <= 8:
                    if board[x + 1, y] == WHITE or \
                            (x + 1, y) in CAMPS or \
                            (x + 1, y) == CASTLE:
                        return True
                if direction == "LEFT" and y - 1 >= 0:
                    if board[x, y - 1] == WHITE or \
                            (x, y - 1) in CAMPS or \
                            (x, y - 1) == CASTLE:
                        return True
                elif y + 1 <= 8:
                    if board[x, y + 1] == WHITE or \
                            (x, y + 1) in CAMPS or \
                            (x, y - 1) == CASTLE:
                        return True
                        # THIRD CASE : the opponent attacked is a white soldier
        else:
            # white soldier case
            direction = self.get_direction(enemy_spot, dest_move)
            if direction == "UP" and x - 1 >= 0:
                if board[x - 1, y] == BLACK or \
                        (x - 1, y) in CAMPS or \
                        (x - 1, y) == CASTLE:
                    return True
            if direction == "DOWN" and x + 1 <= 8:
                if board[x + 1, y] == BLACK or \
                        (x + 1, y) in CAMPS or \
                        (x + 1, y) == CASTLE:
                    return True
            if direction == "LEFT" and y - 1 >= 0:
                if board[x, y - 1] == BLACK or \
                        (x, y - 1) in CAMPS or \
                        (x, y - 1) == CASTLE:
                    return True
            elif y + 1 <= 8:
                if board[x, y + 1] == BLACK or \
                        (x, y + 1) in CAMPS or \
                        (x, y + 1) == CASTLE:
                    return True
        return False

    def convert_list_moves(self, moves):
        """
        This method converts a dict of moves in a list of moves
        Ex
        input = {(a,b): [(c,d), (e,f)]
        output [((a,b),(c,d),((a,b),(e,f))]
        """
        convert_moves = []
        for start in moves.keys():
            for end in moves[start]:
                convert_moves.append((start, end))
        return convert_moves

    def get_standard_moves(self, board):
        if self.color == "WHITE":
            moves_pawn, moves_king = self.legalMoves(board)[0], self.legalMoves(board)[1]
            return self.convert_list_moves(moves_pawn) + self.convert_list_moves(moves_king)
        # if color is black only pawn moves
        return self.convert_list_moves(self.legalMoves(board))





