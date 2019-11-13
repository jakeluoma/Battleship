from Board import Board


class UserProfile:
    def __init__(self, user_name):
        self.user_name = user_name


class User:
    def __init__(self, user_name):
        pass

    # Takes a turn in the game - involving making a guess and striking the opponent's board.
    # Returns whether the move results in victory
    def take_turn(self) -> bool:
        victory = False

        return victory

    def set_boards(self, board: Board, opponent_board: Board) -> None:
        self.board = board
        self.opponent_board = opponent_board