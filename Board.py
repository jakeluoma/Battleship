from Tile import *
from Coordinate import Coordinate

from typing import List
from typing import Tuple

# Provides a board abstraction to a User.  The user may only interact with
# the Board's tiles, protected by the Board.  The 0,0 location is in the
# upper left corner.
class Board:
    def __init__(self, boardDimension: int):
        self.boardDimension = boardDimension
        self.boardTiles: List[List[Tile]] = [[] for i in range(boardDimension)]
        for row in range(boardDimension):
            for col in range(boardDimension):
                self.boardTiles[row].append(Tile(Coordinate(row, col)))

    def getDimension(self) -> int:
        return self.boardDimension

    def getTile(self, row: int, column: int) -> Tile:
        if row >= self.boardDimension or column >= self.boardDimension:
            return None
        if row < 0 or column < 0:
            return None
        return self.boardTiles[row][column]

    # returns true if the given Tile contains a ship, else returns false
    def tileContainsShip(self, tile: Tile) -> bool:
        if tile.getShip() is not None:
            return True
        else:
            return False

    # checks if there is no ship on any of the tiles in the given run.  If ship,
    # returns true.  Else returns false.
    def shipInRun(self, run: List[Tile]) -> bool:
        ship = False
        for tile in run:
            if tile.getShip() is not None:
                ship = True
                break
        return ship

    # checks if any tiles in the given run have been attacked.  If attacked,
    # returns true.  Else returns false.
    def attackInRun(self, run: List[Tile]) -> bool:
        attack = False
        for tile in run:
            if tile.getHitStatus() != TileHitStatus.EMPTY:
                attack = True
                break
        return attack

    # returns true if a ship can be placed on the given Tiles, else returns false
    def validShipPlacement(self, tiles: List[Tile]) -> bool:
        for tile in tiles:
            if self.tileContainsShip(tile):
                return False
        return True

    """Attack Processing Functions"""
    # given a list of coordinates, determines which coordinates were hits
    # and which coordinates were misses.  Returns them as separate lists.
    def processIncomingAttack(self, coordinates: List[Coordinate]) -> Tuple[List[Coordinate], List[Coordinate]]:
        hits: List[Coordinate] = []
        misses: List[Coordinate] = []
        for coordinate in coordinates:
            row, col = coordinate.getRowAndColumn()
            tile = self.getTile(row, col)
            if tile is None:
                continue
            if tile.getShip() is not None:
                hits.append(coordinate)
                tile.setHitStatus(TileHitStatus.HIT)
            else:
                misses.append(coordinate)
                tile.setHitStatus(TileHitStatus.MISS)
        return hits, misses

    # updates the boardTiles to reflect the given hit coordinates and miss
    # coordinates
    def updateHitsAndMisses(self, hits: List[Coordinate], misses: List[Coordinate]):
        for hit in hits:
            row, col = hit.getRowAndColumn()
            tile = self.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.HIT)
        for miss in misses:
            row, col = miss.getRowAndColumn()
            tile = self.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.MISS)