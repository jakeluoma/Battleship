from abc import ABC
from typing import List

from Board import Board
from Coordinate import Coordinates
from Ship import ShipType, Ship, ShipFactory
from player import Player


class Game:
    # Takes in each player
    def __init__(self, user_name: str, opponent_type: str, board_dimensions: int):
        self.player_board = Board(board_dimensions)
        self.opponent_board = Board(board_dimensions)
        self.player = Player(user_name)
        self.opponent = AIFactory.generateAI(opponent_type)
        self.player.set_boards(self.player_board, self.opponent_board)
        self.opponent.set_boards(self.opponent_board, self.player_board)

    # Creates a new board on behalf of a player
    def create_board(self, board_dimensions):
        return Board(board_dimensions)

    def switch_player(self, current_player):
        if not current_player or current_player == self.opponent:
            return self.player
        return self.opponent

    # Alternates between player's turns. Continues loop as long as no player has achieved victory
    def run_game(self):
        current_player = self.player
        while not self.current_player.take_turn():
            self.switch_player(current_player)
        self.end_game()

    # Prints Victory screen and ends game
    def end_game(self):
        pass



