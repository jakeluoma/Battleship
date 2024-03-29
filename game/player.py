from enum import Enum
from typing import List, Union
from typing import Tuple

from components.tile import Coordinate
from game.player_logic import PlayerLogic
from components.ship import Ship, ShipType
from components.board import Board

from stats import statistics
# need to do import statistics due to circular import with statistics
from view.options import MenuOption


class UserProfile:
    def __init__(self, user_name: str):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name


class AIType(Enum):
    LEVEL_EASY = 0
    LEVEL_HARD = 1


class Player:
    def __init__(self, user_profile: UserProfile, player_logic: PlayerLogic, fleet_board: Board, target_board: Board,
                 ships_to_place: List[ShipType], is_ai=False):
        self.user_profile = user_profile
        self.player_logic = player_logic # delegates decision-making to the player_logic class via the Strategy pattern
        self.fleet_board = fleet_board
        self.target_board = target_board
        self.is_ai = is_ai

        self.enemy_ships_sunk = 0
        self.ships_to_place = ships_to_place
        self.num_enemy_ships = len(self.ships_to_place)

        self.player_ships_lost = List[Ship]
        self.player_ships_lost = []
        self.fleet = []
        self.victory = False

    def position_ship(self, ship_type: ShipType):
        ship = self.player_logic.place_ship(self.fleet_board, ship_type)

        self.fleet.append(ship)
        return ship

    # Place the ships
    def position_fleet(self) -> List[Ship]:
        for ship_type in self.ships_to_place:
            self.position_ship(ship_type)
        return self.fleet

    # Set reference to opponent. Since both Players can't be initialized and have their reference to each other set
    # at the same time, a setOpponent() method is required to complete initialization.
    def setOpponent(self, opponent: 'Player'):
        self.opponent = opponent

    # Takes a turn in the game - involving making a guess and striking the opponent's board.
    # Returns whether the move results in victory
    def take_turn(self) -> Union[MenuOption, Tuple[List[Coordinate], List[Coordinate], List[Ship]]]:
        ret = self.player_logic.select_attack(self.target_board)
        if isinstance(ret, MenuOption):
            return ret
        hits, misses, ships_lost = self.opponent.receive_attack([ret])
        self.target_board.update_hits_and_misses(hits, misses)

        if self.user_profile is not None:
            statistics.Statistics.update_stats(self.user_profile.get_user_name(), len(hits), len(misses), len(ships_lost), True)
        
        self.enemy_ships_sunk += len(ships_lost)
        if self.enemy_ships_sunk >= self.num_enemy_ships:
            self.victory = True

        return hits, misses, ships_lost

    def is_victorious(self) -> bool:
        return self.victory

    # returns a list of hit coordinates, a list of miss coordinates, and the number of ships sunk by the attack
    def receive_attack(self, coordinates: List[Coordinate]) -> Tuple[List[Coordinate], List[Coordinate], List[Ship]]:
        hits, misses = self.fleet_board.process_incoming_attack(coordinates)

        ships_lost = []
        for ship in self.fleet:
            if ship.is_sunk():
                ships_lost.append(ship)
        self.player_ships_lost.extend(ships_lost)

        for ship in ships_lost:
            self.fleet.remove(ship)

        if self.user_profile is not None:
            statistics.Statistics.update_stats(self.user_profile.get_user_name(), len(hits), len(misses), len(ships_lost), False)

        return hits, misses, ships_lost
