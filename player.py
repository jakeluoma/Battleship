from enum import Enum
from typing import List
from typing import Tuple

from Coordinate import Coordinate
from PlayerLogic import PlayerLogic
from Ship import Ship, ShipType
from board import Board


class UserProfile:
    # should really have a reference to Statistics
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
        self.player_logic = player_logic
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
    def take_turn(self) -> Tuple[List[Coordinate], List[Coordinate], List[Ship]]:
        hits, misses, ships_lost = self.opponent.receive_attack([self.player_logic.select_attack(self.target_board)])
        self.target_board.update_hits_and_misses(hits, misses)
        # should update statistics here
        
        self.enemy_ships_sunk += len(ships_lost)
        if self.enemy_ships_sunk >= self.num_enemy_ships:
            self.victory = True

        return hits, misses, ships_lost

    def is_victorious(self) -> bool:
        return self.victory

    # returns a list of hit coordinates, a list of miss coordinates, and the number of ships sunk by the attack
    def receive_attack(self, coordinates: List[Coordinate]) -> Tuple[List[Coordinate], List[Coordinate], List[Ship]]:
        hits, misses = self.fleet_board.process_incoming_attack(coordinates)
        # should update statistics here

        ships_lost = []
        for ship in self.fleet:
            if ship.is_sunk():
                ships_lost.append(ship)
        self.player_ships_lost.extend(ships_lost)

        num_ships_sunk_this_turn = 0
        for ship in ships_lost:
            if ship in self.fleet:
                self.fleet.remove(ship)
                num_ships_sunk_this_turn += 1

        return hits, misses, ships_lost
