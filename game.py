from abc import ABC
from enum import Enum
from typing import List

from Board import Board
from Ship import ShipType
from player import Player, UserProfile
from PlayerLogic import CommandLineInstruction, AI


class GameMode(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Game:
    mode_to_dimension_map = {GameMode.EASY: 5, GameMode.MEDIUM: 10, GameMode.HARD: 20}

    def __init__(self, user_profile: UserProfile, game_mode: GameMode):
        # initialize human player
        fleet_board = Board(self.mode_to_dimension(game_mode))
        target_board = Board(self.mode_to_dimension(game_mode))
        self.player1 = Player(user_profile, CommandLineInstruction(), fleet_board, target_board,
                              self.mode_to_ship_types(game_mode))

        # initialize AI player
        fleet_board = Board(game_mode.getBoardDimension())
        target_board = Board(game_mode.getBoardDimension())
        self.player2 = Player(user_profile, AI(), fleet_board, target_board, game_mode.getShipTypes())

        # set each Player's opponent to finish Player initialization
        self.player1.setOpponent(self.player2)
        self.player2.setOpponent(self.player1)

        # human player will start first
        self.current_player = self.player1

    # Switch the current player
    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    # Alternates between players' turns. Continues loop as long as no player has achieved victory
    def run_game(self):
        while not self.current_player.take_turn():
            self.switch_player()
        self.end_game()

    # Prints Victory or Loss screen and ends game
    def end_game(self):
        if self.current_player == self.player1:
            pass # victory screen
        else:
            pass # loss screen
        pass

    def mode_to_dimension(self, gm: GameMode):
        return self.mode_to_dimension_map[gm]

    def mode_to_ship_types(self, gm: GameMode) -> List[ShipType]:
        pass
