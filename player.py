from typing import List
from typing import Tuple

from Board import Board
from Coordinate import Coordinate
from PlayerLogic import PlayerLogic
from Ship import ShipBuilder, Ship, ShipType, ShipBuilder
from Tile import Tile


class UserProfile:
    # should really have a reference to Statistics
    def __init__(self, user_name: str):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name

class Player:
    def __init__(self, user_profile: UserProfile, player_logic: PlayerLogic, fleet_board: Board, target_board: Board, ships_to_place: List[ShipType]):
        self.user_profile = user_profile
        self.player_logic = player_logic
        self.fleet_board = fleet_board
        self.target_board = target_board

        self.enemy_ships_sunk = 0
        self.num_enemy_ships = len(ships_to_place)

        self.player_fleet = self.position_fleet(ships_to_place)
        self.player_ships_lost = List[Ship]

    # Place the ships
    def position_fleet(self, ships_to_place: List[ShipType]) -> List[Ship]:
        fleet = List[Ship]
        for ship in ships_to_place:
            fleet.append(self.player_logic.place_ship(self.fleet_board, ship))
        return fleet

    # Set reference to opponent. Since both Players can't be initialized and have their reference to each other set at the same time,
    # a setOpponent() method is required to complete initialization.
    def setOpponent(self, opponent: 'Player'):
        self.opponent = opponent

    # Takes a turn in the game - involving making a guess and striking the opponent's board.
    # Returns whether the move results in victory
    def take_turn(self) -> bool:
        hits, misses, num_ships_sunk = self.opponent.receive_attack(self.player_logic.select_attack(self.target_board))
        self.target_board.updateHitsAndMisses(hits, misses)
        # should update statistics here
        
        victory = False
        self.enemy_ships_sunk += num_ships_sunk
        if self.enemy_ships_sunk >= self.num_enemy_ships:
            victory = True
        return victory

    # returns a list of hit coordinates, a list of miss coordinates, and the number of ships sunk by the attack
    def receive_attack(self, coordinates: List[Coordinate]) -> Tuple[List[Coordinate], List[Coordinate], int]:
        hits, misses = self.fleet_board.process_incoming_attack(coordinates)
        # should update statistics here

        for ship in self.player_fleet:
            if ship.is_sunk():
                self.player_ships_lost.append(ship)

        num_ships_sunk_this_turn = 0
        for ship in self.player_ships_lost:
            if ship in self.player_fleet:
                self.player_fleet.remove(ship)
                num_ships_sunk_this_turn += 1

        return hits, misses, num_ships_sunk_this_turn
