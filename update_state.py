# File which contains the class with the game rules.
import copy
import numpy as np
import player
EMPTY = 0
WHITE = 1
BLACK = 2
KING = 3


CAMPS = ((0, 3), (0, 4), (0, 5), (1, 4), 
         (3, 0), (4, 0), (5, 0), (4, 1),
         (8, 3), (8, 4), (8, 5), (7, 4),
         (4, 7), (3, 8), (4, 8), (5, 8))

CASTLE = (4, 4)

CASTLE_NEIGHBOUR = ((4, 3), (4, 5), (3, 4), (5, 4))


class UpdateBoard:
    '''
    USAGE : 
       CREATE THE OBJECT USING THE BOARD AND THE ACTION
       OBTAIN THE NEW BOARD (DEEP COPY) CALLING THE FUNCTION board_updater()  
    '''
    def __init__(self, board, action):
        '''
        board --> np.arry in the from defined in converter.
        action --> move in the numeric form [(row, col), (row, col)] 
                   where the first element is the starting point and the second the arrive
        '''
        self.board = board
        self.action = action
        self.__start_coord = action[0] 
        self.__dest_coord = action[1]
        self.coord_to_check = self.add_coord()
        if self.board[self.__start_coord[0], self.__start_coord[1]] == WHITE or \
           self.board[self.__start_coord[0], self.__start_coord[1]] == KING:
            self.who_played = WHITE
        else :
            self.who_played = BLACK
    
    def add_coord(self):
        '''
        return attributes up, down, right, left if are in the board
        '''
        coord_to_check = {}
        if self.__dest_coord[0] != 0: 
            coord_to_check["UP"] = (self.__dest_coord[0] - 1, self.__dest_coord[1])
        if self.__dest_coord[0] != 8:
            coord_to_check["DOWN"] = (self.__dest_coord[0] + 1, self.__dest_coord[1])
        if self.__dest_coord[1] != 0:
            coord_to_check["LEFT"] = (self.__dest_coord[0], self.__dest_coord[1] - 1)
        if self.__dest_coord[1] != 8:
            coord_to_check["RIGHT"] = (self.__dest_coord[0], self.__dest_coord[1] + 1)
        return coord_to_check
    
    def board_updater(self):
        '''
        return the new state generated by the move
        '''
        new_board = copy.deepcopy(self.board)
        # Lets move the piece 
        new_board[self.__start_coord[0], self.__start_coord[1]] = EMPTY 
        new_board[self.__dest_coord[0], self.__dest_coord[1]] = self.who_played
        # Get the near enemies
        enemies = self.check_near_enemies()
        if len(enemies) != 0:
            for enemy_spot in enemies:
                take_out = self.take(enemy_spot)
                if take_out == True:
                    new_board[enemy_spot[0], enemy_spot[1]] = EMPTY
        return new_board    

    def take(self, enemy_spot):
        '''
        Check if the near enemy has to be taken out 
        '''
        x = enemy_spot[0]
        y = enemy_spot[1] 
        take_out = False

        # FIRST CASE : the opponent which is attacked is the king
        if self.board[x, y] == KING:
            # Check its postition
            if (x, y) == CASTLE:
                if self.board[x + 1, y] == BLACK and \
                self.board[x - 1, y] == BLACK and \
                self.board[x, y + 1] == BLACK and \
                self.board[x, y - 1] == BLACK:
                   take_out = True

            elif (x, y) in CASTLE_NEIGHBOUR:
                neighbours_count = 0
                for coords in CASTLE_NEIGHBOUR:
                    if self.board[coords[1], coords[0]] == BLACK:
                        neighbours_count += 1
                if neighbours_count >= 3:
                    take_out = True
            else :
                # KING isn't in the castle or in its neighbourhood
                # He is taken out as a simple soldier
                direction = self.get_direction(enemy_spot)
                if direction == "UP" and x - 1 >= 0:
                    if self.board[x - 1, y] == BLACK or \
                       (x - 1, y) in CAMPS or \
                       (x - 1, y) == CASTLE:
                        take_out = True
                if direction == "DOWN" and x + 1 <= 8:
                    if self.board[x + 1, y] == BLACK or \
                       (x + 1, y) in CAMPS or \
                       (x + 1, y) == CASTLE:
                        take_out = True
                if direction == "LEFT" and y - 1 >= 0:
                    if self.board[x, y - 1] == BLACK or \
                       (x, y - 1) in CAMPS or \
                       (x, y - 1) == CASTLE:
                        take_out = True 
                elif y + 1 <= 8:
                    if self.board[x, y + 1] == BLACK or \
                        (x, y + 1) in CAMPS or \
                        (x, y + 1) == CASTLE:
                        take_out = True
        # SECOND CASE : the opponent which is attacked is a black soldier   
        elif self.board[enemy_spot[0], enemy_spot[1]] == BLACK:
            if (x, y) not in CAMPS:
                direction = self.get_direction(enemy_spot)
                if direction == "UP" and x - 1 >= 0:
                    if self.board[x - 1, y] == WHITE or \
                       (x - 1, y) in CAMPS or \
                       (x - 1, y) == CASTLE:
                        take_out = True
                if direction == "DOWN" and x + 1 <= 8:
                    if self.board[x + 1, y] == WHITE or \
                       (x + 1, y) in CAMPS or \
                       (x + 1, y) == CASTLE:
                        take_out = True
                if direction == "LEFT" and y - 1 >= 0:
                    if self.board[x, y - 1] == WHITE or \
                       (x, y - 1) in CAMPS or \
                       (x, y - 1) == CASTLE:
                        take_out = True
                elif y + 1 <= 8:
                    if self.board[x, y + 1] == WHITE or \
                        (x, y + 1) in CAMPS or \
                        (x, y - 1) == CASTLE:
                        take_out = True    
        # THIRD CASE : the opponent attacked is a white soldier
        else :
            #white soldier case
            direction = self.get_direction(enemy_spot)
            if direction == "UP" and x - 1 >= 0:
                if self.board[x - 1, y] == BLACK or \
                    (x - 1, y) in CAMPS or \
                    (x - 1, y) == CASTLE:
                    take_out = True
            if direction == "DOWN" and x + 1 <= 8:
                if self.board[x + 1, y] == BLACK or \
                    (x + 1, y) in CAMPS or \
                    (x + 1, y) == CASTLE:
                    take_out = True
            if direction == "LEFT" and y - 1 >= 0:
                if self.board[x, y - 1] == BLACK or \
                    (x, y - 1) in CAMPS or \
                    (x, y - 1) == CASTLE:
                    take_out = True 
            elif y + 1 <= 8:
                if self.board[x, y + 1] == BLACK or \
                    (x, y + 1) in CAMPS or \
                    (x, y + 1) == CASTLE:
                    take_out = True
        return take_out
            

    def get_direction(self, enemy_spot):
        x_en, y_en = enemy_spot
        x_al, y_al = self.__dest_coord
        if x_en == x_al:
            if y_en == y_al + 1:
                direction = 'RIGHT'
            else :
                direction = 'LEFT'
        else :
            #Same Y
            if x_en == x_al + 1:
                direction = "UP"
            else :
                direction = 'DOWN'
        return direction




    def check_near_enemies(self):
        '''
        return a list of tuples with the coord of the opponent soldiers that could be taken out (the one near it)
        (it could be empty)
        ''' 
        enemies = []
        if self.who_played == WHITE:
            for key in self.coord_to_check:
                if self.board[self.coord_to_check[key][0], self.coord_to_check[key][1]] == BLACK:
                    enemies.append(self.coord_to_check[key])
        else :
            for key in self.coord_to_check:
                if self.board[self.coord_to_check[key][0], self.coord_to_check[key][1]] == WHITE or \
                   self.board[self.coord_to_check[key][0], self.coord_to_check[key][1]] == KING :
                    enemies.append(self.coord_to_check[key]) 
        return enemies


    