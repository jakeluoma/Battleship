from abc import ABC
from typing import List

from Board import Board, Direction
from Coordinate import Coordinates
from Ship import ShipFactory, Ship, ShipType
from Tile import Tile


class UserProfile:
    def __init__(self, user_name):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name


class PlayerLogic(ABC):
    ship_factory = None

    def __init__(self, ship_factory: ShipFactory):
        self.ship_factory = ship_factory
        self.fleet = []

    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        pass

    def select_attack(self, target_board: Board) -> Coordinates:
        pass


class CommandLineInstruction(PlayerLogic):
    pass

class Player:
    def __init__(self, user_name, player_logic: PlayerLogic = CommandLineInstruction):
        self.user_name = user_name
        self.player_logic = player_logic
        self.player_fleet = []
        #self.enemy_fleet = [] Not sure why this is required?

    def set_boards(self, player_board: Board, opponent_board: Board) -> None:
        self.player_board = player_board
        self.opponent_board = opponent_board

    def select_fleet(self) -> List[Ship]:
        pass

    def position_fleet(self) -> None:
        for ship in self.player_fleet:
            self.place_ship(ship)

    def place_ship(self, ship: ShipType):
        self.player_logic.place_ship(self.player_board, ship)

    # Takes a turn in the game - involving making a guess and striking the opponent's board.
    # Returns whether the move results in victory
    def take_turn(self) -> bool:
        victory = False
        return victory

    def recieve_attack(self, coordinates: Coordinates):
        self.player_board.processIncomingAttack(coordinates)
        self.player_board.updateHitsAndMisses()
