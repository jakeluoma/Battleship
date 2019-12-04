from abc import ABC
from enum import Enum
from typing import List

import pickle

from board import Board
from Ship import ShipType
from player import Player, UserProfile
from PlayerLogic import CommandLineInstruction, AI


class GameMode():
    def __init__(self):
        self.board_dimension = 10
        self.ship_types: List[ShipType] = [ShipType.BATTLESHIP, ShipType.CARRIER, ShipType.DESTROYER, ShipType.PATROL_BOAT, ShipType.SUBMARINE]

    def get_dimension(self) -> int:
        return self.board_dimension

    def get_ship_types(self) -> List[ShipType]:
        return self.ship_types

class Game:
    def __init__(self, user_profile: UserProfile, game_mode: GameMode):
        # initialize human player
        fleet_board = Board(game_mode.get_dimension())
        target_board = Board(game_mode.get_dimension())
        self.player1 = Player(user_profile, CommandLineInstruction(), fleet_board, target_board,
                              game_mode.get_ship_types())

        # initialize AI player
        fleet_board = Board(game_mode.get_dimension())
        target_board = Board(game_mode.get_dimension())
        self.player2 = Player(user_profile, AI(), fleet_board, target_board, game_mode.get_ship_types())

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
        """ somewhere in here is where you'd probably want to display the canvas asking whether the player wants
            to attack or save and exit.  If saving and exiting, should call save_game() and then return"""
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

    # saves game to pickle, which gets written to file
    def save_game(self):
        # player1 is the human user
        file_name = self.player1.user_profile.get_user_name() + "_saved_game.p"
        try:
            pickle.dump(self, open(file_name, "wb"))
        except:
            print("Failed to save game")

    # intended to be called by a non-Game instance.  Loads a saved game from a pickle
    # and returns a Game instance.
    @staticmethod
    def load_saved_game(user: UserProfile):
        file_name = user.get_user_name() + "_saved_game.p"
        try:
            return pickle.load(open(file_name, "rb"))
        except:
            print("Failed to load game")
            return None
