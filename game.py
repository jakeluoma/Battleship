from abc import ABC
from typing import List

from Board import Board
from Coordinate import Coordinates
from Ship import ShipType, Ship, ShipFactory
from player import Player, UserProfile
from PlayerLogic import CommandLineInstruction, AI

# TODO
class GameMode:
    def __init__(self):
        pass

    def getBoardDimension(self) -> int:
        pass

    def getShipTypes(self) -> List[ShipType]:
        pass

class Game:
    def __init__(self, user_profile: UserProfile, game_mode: GameMode):
        # initialize human player
        fleet_board = Board(game_mode.getBoardDimension())
        target_board = Board(game_mode.getBoardDimension())
        self.player1 = Player(user_profile, CommandLineInstruction(), fleet_board, target_board, game_mode.getShipTypes())

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



