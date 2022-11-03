from aima.games import *
from state_manager import State_Manager

class TablutGame(Game):

    def __init__(self, color, timeout, board, king_postion):
        self.manager = State_Manager(color, timeout, king_postion)
        self.initial = GameState(to_move=color,
                                 utility=self.manager.goal_state(board),
                                 board= board,
                                 moves=self.manager.get_standard_moves(board) )
        self.timeout = timeout


    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        return self.manager.get_standard_moves(state.board)


    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        # Changing board status -- > Kilian
        board = state.board
        self.manager.make_move(board, move)

        new_color = ("BLACK" if state.to_move == "WHITE" else "WHITE")
        self.manager.set_color(new_color)
        return GameState(to_move=new_color,
                         utility=self.manager.goal_state(board),
                         board= board, # mettere quella nuova
                         moves=self.manager.get_standard_moves(board))



    def utility(self, state, player):
        """Return the value of this final state to player.
        1 for win, -1 for loss, 0 otherwise.
        """
        return state.utility if player == "WHITE" else -state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.utility != 0

