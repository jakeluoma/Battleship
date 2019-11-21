from typing import List

from Board import Board
from Coordinate import Coordinate
from Ship import ShipBuilder, Ship, ShipType
from Tile import Tile


class UserProfile:
    def __init__(self, user_name):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name

class Player:
    def __init__(self, user_name, player_logic: PlayerLogic = CommandLineInstruction):
        self.user_name = user_name
        self.player_logic = player_logic
        self.player_fleet = []
        #self.enemy_fleet = [] Not sure why this is required? #JEL: with the way we're implementing ships/tiles, this is no longer required

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

    def recieve_attack(self, coordinate: Coordinate):
        self.player_board.processIncomingAttack(coordinate)
        self.player_board.updateHitsAndMisses()
