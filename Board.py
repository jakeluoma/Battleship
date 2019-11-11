from Tile import *
from Coordinate import *

# Provides a board abstraction to a User.  The user may only interact with
# the Board's tiles, protected by the Board.
class Board:
    boardDimension = 0
    boardTiles = []

    def __init__(self, boardDimension):
        self.boardDimension = boardDimension
        for row in range(boardDimension):
            boardTiles.append([])
            for col in range(boardDimension):
                boardTiles[row].append(Tile(Coordinate(row, col)))

    def getTile(self, row, column):
        if row >= self.boardDimension or column >= self.boardDimension:
            return None
        if row < 0 or column < 0:
            return None
        return self.boardTiles[row][column]

    """ Ship Placement Functions"""
    # returns true if the given Tile contains a ship, else returns false
    def tileContainsShip(self, tile):
        if tile.getShip() is not None:
            return True
        else:
            return False
    
    # returns true if a ship can be placed on the given Tiles, else returns false
    def validShipPlacement(self, tiles):
        for tile in tiles:
            if self.tileContainsShip(tile):
                return False
        return True

    # returns true if the ship was placed on the desired tiles, else returns false
    def placeShip(self, ship, desiredTiles):
        if self.validShipPlacement(desiredTiles):
            ship.setTiles(desiredTiles)
            for tile in desiredTiles:
                tile.setShip(ship)
            return True
        else:
            return False

    """ Ship Placement Helper Functions for Client"""
    # returns two lists of lists (aka runs) of tiles of length n.  The first returned
    # list contains the horizontal runs, the second contains the vertical runs.  None 
    # of the tiles in a given run contain a ship.
    def getRunsOfTilesWithNoShipLengthN(self, n):
        horizontal = []
        vertical = []

        # check for horizontal runs
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                possibleRun = []
                for i in range(n):
                    colIndex = i + col
                    tile = boardTiles.getTile(row, colIndex)
                    if tile is None:
                        break
                    if tile.getShip() is not None:
                        break
                    else:
                        possibleRun.append(tile)
                if len(possibleRun) == n:
                    horizontal.append(possibleRun)

        # check for vertical runs
        for col in range(self.boardDimension):
            for row in range(self.boardDimension):
                possibleRun = []
                for i in range(n):
                    rowIndex = i + row
                    tile = boardTiles.getTile(rowIndex, col)
                    if tile is None:
                        break
                    if tile.getShip() is not None:
                        break
                    else:
                        possibleRun.append(tile)
                if len(possibleRun) == n:
                    vertical.append(possibleRun)

        return horizontal, vertical
    
    # gets tiles adjacent to the given tile.  Will only return tiles that
    # are within the board.
    def getAdjacentTiles(self, tile):
        ret = []
        locations = []
        row, col = tile.getRowAndColumn()
        locations.append((row + 1, col))
        locations.append((row - 1, col))
        locations.append((row, col + 1))
        locations.append((row, col - 1))

        for location in locations:
            tile = self.getTile(*location)
            if tile is not None:
                ret.append(tile)

        return ret

    # returns two lists of lists (aka runs) of tiles of length n.  The first returned
    # list contains the horizontal runs, the second contains the vertical runs.  None 
    # of the tiles in a given run contain a ship.  The runs must have at least one
    # tile adjacent to a tile that already contains a ship.
    def getRunsOfTilesWithNoShipLengthNNextToShip(self, n):
        # find tiles that already have ships
        tilesWithShips = []
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                tile = boardTiles.getTile(row, col)
                if tile is None:
                    continue
                if tile.getShip() is not None:
                    tilesWithShips.append(tile)
        
        startingTiles = []
        for tile in tilesWithShips:
            adjacentTiles = self.getAdjacentTiles(tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.getShip() is None:
                    startingTiles.append(adjacentTile)
        list(set(startingTiles)) # get rid of duplicates

        # TODO
        # from each starting tile, try to get a run of length N in each direction
        # may be worth making a helper method to get a run of length n given a starting tile
        # and a direction.  Then refactor getRunsofTilesWithNoShipOfLengthN.  Put the
        # checking for no ship, or no shot in the wrapper methods...


    """Attack Processing Functions"""
    # given a list of coordinates, determines which coordinates were hits
    # and which coordinates were misses.  Returns them as separate lists.
    def processIncomingAttack(self, coordinates):
        hits = []
        misses = []
        for coordinate in coordinates:
            row, col = coordinate.getRowAndColumn()
            tile = boardTiles.getTile(row, col)
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
            tile = boardTiles.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.HIT)
        for miss in misses:
            row, col = hit.getRowAndColumn()
            tile = boardTiles.getTile(row, col)
            if tile is None:
                continue
            tile.setHitStatus(TileHitStatus.MISS)

    """ Attack Selection Helper Functions for Client"""


    