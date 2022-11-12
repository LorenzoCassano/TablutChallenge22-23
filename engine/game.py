from aima.games import *
from state_manager import State_Manager

class TablutGame(Game):

    def __init__(self, color, board, king_postion):
        self.manager = State_Manager(color, king_postion)
        self.initial = GameState(to_move=color,
                                 utility=self.manager.heuristics(board),
                                 board= board,
                                 moves=self.manager.legalMoves(board))


    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        self.manager.set_color(state.to_move)
        return self.manager.legalMoves(state.board)


    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        #print("Board di valutazione \n")
        #print(state.board)
        board = state.board

        new_board, win = self.manager.board_updater(board, move)
        #print(new_board)
        #print("\n")
        new_color = ("BLACK" if state.to_move == "WHITE" else "WHITE")
        if win == None:
            win = self.manager.heuristics(new_board)

        self.manager.set_color(new_color)
        return GameState(to_move=new_color,
                         utility= win,
                         board= new_board,
                         moves=self.manager.legalMoves(new_board))



    def utility(self, state, player):
        """Return the value of this final state to player.
        1 for win, -1 for loss, 0 otherwise.
        """
        return state.utility if player == "WHITE" else -state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return state.utility == 1


    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

