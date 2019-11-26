from Tile import *
from Coordinate import Coordinate

from typing import List
from typing import Tuple

# Provides a board abstraction to a User.  The user may only interact with
# the Board's tiles, protected by the Board.  The 0,0 location is in the
# upper left corner.
class Board:
    def __init__(self, board_dimension: int):
        self.board_dimension = board_dimension
        self.boardTiles: List[List[Tile]] = [[] for i in range(board_dimension)]
        for row in range(board_dimension):
            for col in range(board_dimension):
                self.boardTiles[row].append(Tile(Coordinate(row, col)))

    def get_dimension(self) -> int:
        return self.board_dimension

    def get_tile(self, row: int, column: int) -> Tile:
        if row >= self.board_dimension or column >= self.board_dimension:
            return None
        if row < 0 or column < 0:
            return None
        return self.boardTiles[row][column]

    # returns true if the given Tile contains a ship, else returns false
    def tile_contains_ship(self, tile: Tile) -> bool:
        if tile.get_ship() is not None:
            return True
        else:
            return False

    # checks if there is no ship on any of the tiles in the given run.  If ship,
    # returns true.  Else returns false.
    def ship_in_run(self, run: List[Tile]) -> bool:
        ship = False
        for tile in run:
            if tile.get_ship() is not None:
                ship = True
                break
        return ship

    # checks if any tiles in the given run have been attacked.  If attacked,
    # returns true.  Else returns false.
    def attack_in_run(self, run: List[Tile]) -> bool:
        attack = False
        for tile in run:
            if tile.get_hit_status() != TileHitStatus.EMPTY:
                attack = True
                break
        return attack

    # returns true if a ship can be placed on the given Tiles, else returns false
    def valid_ship_placement(self, tiles: List[Tile]) -> bool:
        for tile in tiles:
            if self.tile_contains_ship(tile):
                return False
        return True

    """Attack Processing Functions"""
    # given a list of coordinates, determines which coordinates were hits
    # and which coordinates were misses.  Returns them as separate lists.
    def process_incoming_attack(self, coordinates: List[Coordinate]) -> Tuple[List[Coordinate], List[Coordinate]]:
        hits: List[Coordinate] = []
        misses: List[Coordinate] = []
        for coordinate in coordinates:
            row, col = coordinate.get_row_and_column()
            tile = self.get_tile(row, col)
            if tile is None:
                continue
            if tile.get_ship() is not None:
                hits.append(coordinate)
                tile.set_hit_status(TileHitStatus.HIT)
            else:
                misses.append(coordinate)
                tile.set_hit_status(TileHitStatus.MISS)
        return hits, misses

    # updates the boardTiles to reflect the given hit coordinates and miss
    # coordinates
    def update_hits_and_misses(self, hits: List[Coordinate], misses: List[Coordinate]):
        for hit in hits:
            row, col = hit.get_row_and_column()
            tile = self.get_tile(row, col)
            if tile is None:
                continue
            tile.set_hit_status(TileHitStatus.HIT)
        for miss in misses:
            row, col = miss.get_row_and_column()
            tile = self.get_tile(row, col)
            if tile is None:
                continue
            tile.set_hit_status(TileHitStatus.MISS)