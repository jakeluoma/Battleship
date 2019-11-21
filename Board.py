from Tile import *
from Coordinate import Coordinates

from typing import List



# Provides a board abstraction to a User.  The user may only interact with
# the Board's tiles, protected by the Board.  The 0,0 location is in the
# upper left corner.
class Board:
    boardDimension = 0
    boardTiles = List[List[Tile]]

    def __init__(self, boardDimension: int):
        self.boardDimension = boardDimension
        for row in range(boardDimension):
            self.boardTiles.append([])
            for col in range(boardDimension):
                self.boardTiles[row].append(Tile(Coordinates(row, col)))

    def getDimension(self) -> int:
        return self.boardDimension

    def getTile(self, row: int, column: int) -> Tile:
        if row >= self.boardDimension or column >= self.boardDimension:
            return None
        if row < 0 or column < 0:
            return None
        return self.boardTiles[row][column]

    # returns true if a ship can be placed on the given Tiles, else returns false
    def validShipPlacement(self, tiles):
        for tile in tiles:
            if self.tileContainsShip(tile):
                return False
        return True

    """Attack Processing Functions"""
    # given a list of coordinates, determines which coordinates were hits
    # and which coordinates were misses.  Returns them as separate lists.
    def processIncomingAttack(self, coordinates):
        hits = []
        misses = []
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
    def updateHitsAndMisses(self, hits, misses):
        for hit in hits:
            row, col = hit.getRowAndColumn()
            tile = self.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.HIT)
        for miss in misses:
            row, col = hit.getRowAndColumn()
            tile = self.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.MISS)