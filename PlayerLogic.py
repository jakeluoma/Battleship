from abc import ABC
from enum import Enum
from typing import List, Optional
from typing import Tuple
from random import randrange

from Board import Board, BoardHelper
from Coordinate import Coordinate
from Ship import ShipBuilder, Ship, ShipType
from Tile import Tile, TileHitStatus
from view import View


class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


class PlayerLogic(ABC):
    def __init__(self):
        self.ship_builder = ShipBuilder()
        self.view = View()

    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        pass

    def select_attack(self, target_board: Board) -> Coordinate:
        pass


""" Player Control """


class CommandLineInstruction(PlayerLogic):
    def __init__(self):
        super()
        self.num_ships_placed = 0
    
    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        """
        I'm proposing that getting user input be handled by the view.
        Some Likely Pseudocode:

        self.ship_builder.startShip(ship_type)

        make a ship-placing canvas that says which ship is being placed and prompts for a coordinate
        self.view.paint(canvas)
        coordinate = self.view.getCoordinate()
        make a ship-placing canvas that says which ship is being placed and prompts for a directioon
        self.view.paint(canvas)
        direction = self.view.getDirection()

        calculate the list of desired coordinates and convert into a list of tiles using board.getTile()
        board.validShipPlacement(tiles)
        if valid, self.ship_builder.placeShip(tiles) and return self.ship_builder.returnCompeltedShip()
        else loop back to prompting for coordinate and direction.
        """
        self.ship_builder.start_ship(ship_type)

        # Get initial coordinate and direction from shell
        row, col = self.view.get_coordinate()
        direction = self.view.get_direction()
        run = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, self.ship_builder.get_ship_size(), row, col,
                                                                 direction)
        if not run:
            print("Impossible to place ship " + ship_type.name)
            return None

        self.ship_builder.place_ship(run)
        self.num_ships_placed += 1
        return self.ship_builder.return_completed_ship()

    def select_attack(self, target_board: Board) -> Optional[Coordinate]:
        """
        similar to place_ship()... just make the right canvas, give to view, call self.view.getCoordinate(),
        check with board via board.getTile(coordinate) that it's a valid coordinate before returning it.
        """
        # Get attack coordinate from shell
        row, col = self.view.get_coordinate()

        tile = target_board.get_tile(row, col)
        if target_board.attack_in_run([tile]):
           print("This tile has already been hit")
           return None

        return tile.get_coordinate()


""" AI Control """
class AI(PlayerLogic):
    def __init__(self):
        super()
        self.num_ships_placed = 0

    # Places a ship onto the board
    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        self.ship_builder.start_ship(ship_type)

        runs = List[List[Tile]]
        if self.num_ships_placed == 0: # place ship anywhere
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
        return self.ship_builder.return_completed_ship()

    # choose where to attack and return that Coordinate
    def select_attack(self, target_board: Board) -> Coordinate:
        potentialTargetTiles = List[Tile]

        # always attack ends of hit runs if there are any
        potentialTargetTiles = BoardHelper.get_tiles_with_no_attack_at_end_of_hit_runs(target_board)
        if potentialTargetTiles:
            index = randrange(0, len(potentialTargetTiles))
            return potentialTargetTiles[index].get_coordinate()

        # choose whether to attack tiles adjacent to hits, if there are any, or attack randomly
        if randrange(0, 4) < 3:
            # attack tiles adjacent to hits if there are any
            potentialTargetTiles = BoardHelper.get_tiles_with_no_attack_adjacent_to_hits(target_board)
            if potentialTargetTiles:
                index = randrange(0, len(potentialTargetTiles))
                return potentialTargetTiles[index].get_coordinate()

        # attack randomly
        n = 2 # hardcoded to length of patrol boat for now
        potentialTargetTiles = BoardHelper.get_runs_of_tiles_with_no_attack_length_n(target_board, n)
        index = randrange(0, len(potentialTargetTiles))
        return potentialTargetTiles[index][n-1].get_coordinate()