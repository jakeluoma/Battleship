from abc import ABC
from enum import Enum
from typing import List, Optional, Tuple, Union
from random import randrange

from coordinate import Coordinate
from ship import ShipBuilder, Ship, ShipType
from Tile import Tile, TileHitStatus
from board import Board, BoardHelper
from canvas import MenuOption
from view import View

class PlayerLogic(ABC):
    def __init__(self):
        self.ship_builder = ShipBuilder() # implements the Builder pattern to make Ships
        self.view = View() # PlayerLogic implements the Controller part of the MVC pattern

    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        pass

    def select_attack(self, target_board: Board) -> Coordinate:
        pass


""" Player Control """
class CommandLineInstruction(PlayerLogic):
    def __init__(self):
        PlayerLogic.__init__(self)
        self.num_ships_placed = 0
    
    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        self.ship_builder.start_ship(ship_type)

        # get a valid ship placement from the user
        while True:
            row, col = self.view.get_coordinate_or_quit(board).get_row_and_column()
            direction = self.view.get_direction()
            run = BoardHelper.get_run_of_tiles_length_n(board, self.ship_builder.get_ship_size(), row, col, direction)
            if not board.valid_ship_placement(run):
                print("Invalid ship placement.  Try again.")
                continue
            else:
                self.ship_builder.place_ship(run)
                self.num_ships_placed += 1
                return self.ship_builder.return_completed_ship()

    def select_attack(self, target_board: Board) -> Union[Coordinate, MenuOption]:
        # Get attack coordinate from the user
        while True:
            ret = self.view.get_coordinate_or_quit(target_board)
            if isinstance(ret, MenuOption):
                return ret
            row, col = ret.get_row_and_column()
            tile = target_board.get_tile(row, col)
            if not Tile:
                print("Invalid coordinate.  Try again.")
                continue
            if tile.get_hit_status() != TileHitStatus.EMPTY:
                print("Tile already hit.  Try again.")
                continue
            return tile.get_coordinate()


""" AI Control """
class AI(PlayerLogic):
    def __init__(self):
        PlayerLogic.__init__(self)
        self.num_ships_placed = 0
        self.shortest_ship_length = 0

    # Places a ship onto the board
    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        self.ship_builder.start_ship(ship_type)

        runs: List[List[Tile]] = []
        if self.num_ships_placed == 0: # place ship anywhere
            self.shortest_ship_length = self.ship_builder.get_ship_size()
            runs = BoardHelper.get_runs_of_tiles_with_no_ship_length_n(board, self.ship_builder.get_ship_size())
        elif randrange(0, 3) == 0: # maybe place ship next to an already placed ship
            runs = BoardHelper.get_runs_of_tiles_with_no_ship_length_n_next_to_ship(board, self.ship_builder.get_ship_size())
        else: # place ship anywhere
            runs = BoardHelper.get_runs_of_tiles_with_no_ship_length_n(board, self.ship_builder.get_ship_size())

        if len(runs) == 0:
            print("Impossible to place ship " + ship_type.name)
            return None
        index = randrange(0, len(runs)) # pick where to place ship among valid places
        run = runs[index]
        self.ship_builder.place_ship(run)
        self.num_ships_placed += 1
        if self.ship_builder.get_ship_size() < self.shortest_ship_length:
            self.shortest_ship_length = self.ship_builder.get_ship_size()
        return self.ship_builder.return_completed_ship()

    # choose where to attack and return that Coordinate
    def select_attack(self, target_board: Board) -> Coordinate:
        # usually attack ends of hit runs, if there are any
        if randrange(0,4) < 3:
            potentialTargetTiles: List[Tile] = BoardHelper.get_tiles_with_no_attack_at_end_of_hit_runs(target_board)
            if potentialTargetTiles:
                index = randrange(0, len(potentialTargetTiles))
                return potentialTargetTiles[index].get_coordinate()

        # usually attack tiles adjacent to hits, if there are any
        if randrange(0, 4) < 3:
            # attack tiles adjacent to hits if there are any
            potentialTargetTiles = BoardHelper.get_tiles_with_no_attack_adjacent_to_hits(target_board)
            if potentialTargetTiles:
                index = randrange(0, len(potentialTargetTiles))
                return potentialTargetTiles[index].get_coordinate()

        # attack in ideal search pattern
        potentialTargetTiles = BoardHelper.get_ideally_spaced_attack_tiles(target_board, self.shortest_ship_length)
        if potentialTargetTiles:
            index = randrange(0, len(potentialTargetTiles))
            return potentialTargetTiles[index].get_coordinate()