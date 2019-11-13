from Tile import *
from Coordinate import *

# Provides a board abstraction to a User.  The user may only interact with
# the Board's tiles, protected by the Board.  The 0,0 location is in the
# upper left corner.
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
    # returns a run of tiles of length n, given a starting row, column, and direction.  If no
    # run meets that criteria or if an invalid direction is given, returns an empty list.
    # Note that runs are always ordered left to right or up to down.
    def getRunOfTilesLengthN(self, n, row, col, direction):
        run = []
        if direction == "right":
            possibleRun = []
            for i in range(n):
                colIndex = col + i
                tile = self.getTile(row, colIndex)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == "left":
            possibleRun = []
            for i in range(n):
                colIndex = col - i
                tile = self.getTile(row, colIndex)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun
        elif direction == "down":
            possibleRun = []
            for i in range(n):
                rowIndex = row + i
                tile = self.getTile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == "up":
            possibleRun = []
            for i in range(n):
                rowIndex = row - i
                tile = self.getTile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun
        
        return run

    # checks if there is no ship on any of the tiles in the given run.  If no ship,
    # returns true.  Else returns false.
    def noShipInRun(self, run):
        noShip = True
        for tile in run:
            if tile.getShip() is not None:
                noShip = False
                break
        return noShip

    # returns two lists of lists (aka runs) of tiles of length n.  The first returned
    # list contains the horizontal runs, the second contains the vertical runs.  None 
    # of the tiles in a given run contain a ship.
    def getRunsOfTilesWithNoShipLengthN(self, n):
        horizontal = []
        vertical = []

        # check for horizontal runs
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                possibleRun = self.getRunOfTilesLengthN(n, row, col, "right")
                if not possibleRun:
                    break
                if self.noShipInRun(possibleRun):
                    horizontal.append(possibleRun)

        # check for vertical runs
        for col in range(self.boardDimension):
            for row in range(self.boardDimension):
                possibleRun = self.getRunOfTilesLengthN(n, row, col, "down")
                if not possibleRun:
                    break
                if self.noShipInRun(possibleRun):
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
                tile = self.getTile(row, col)
                if tile is None:
                    continue
                if tile.getShip() is not None:
                    tilesWithShips.append(tile)
        
        # starting tiles are tiles without ships adjacent to the tiles that have ships
        startingTiles = []
        for tile in tilesWithShips:
            adjacentTiles = self.getAdjacentTiles(tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.getShip() is None:
                    startingTiles.append(adjacentTile)
        list(set(startingTiles)) # get rid of duplicate tiles

        # from each starting tile, try to get a run of length N in each direction
        horizontal = []
        vertical = []
        for tile in startingTiles:
            row, col = tile.getCoordinate().getRowAndColumn()

            possibleRun = self.getRunOfTilesLengthN(n, row, col, "up")
            if possibleRun:
                if self.noShipInRun(possibleRun):
                    vertical.append(possibleRun)
            
            possibleRun = self.getRunOfTilesLengthN(n, row, col, "down")
            if possibleRun:
                if self.noShipInRun(possibleRun):
                    vertical.append(possibleRun)

            possibleRun = self.getRunOfTilesLengthN(n, row, col, "right")
            if possibleRun:
                if self.noShipInRun(possibleRun):
                    horizontal.append(possibleRun)

            possibleRun = self.getRunOfTilesLengthN(n, row, col, "left")
            if possibleRun:
                if self.noShipInRun(possibleRun):
                    horizontal.append(possibleRun)

        # only want unique runs
        # https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
        horizontal = [list(x) for x in set(tuple(x) for x in horizontal)]
        vertical = [list(x) for x in set(tuple(x) for x in vertical)]

        return horizontal, vertical


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

    """ Attack Selection Helper Functions for Client"""
    # checks if there is no ship on any of the tiles in the given run.  If no ship,
    # returns true.  Else returns false.
    def noAttackInRun(self, run):
        noAttack = True
        for tile in run:
            if tile.getHitStatus() != TileHitStatus.EMPTY:
                noAttack = False
                break
        return noAttack

    # returns two lists of lists (aka runs) of tiles of length n.  The first returned
    # list contains the horizontal runs, the second contains the vertical runs.  None 
    # of the tiles in a given run contain a ship.
    def getRunsOfTilesWithNoAttackLengthN(self, n):
        horizontal = []
        vertical = []

        # check for horizontal runs
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                possibleRun = self.getRunOfTilesLengthN(n, row, col, "right")
                if not possibleRun:
                    break
                if self.noAttackInRun(possibleRun):
                    horizontal.append(possibleRun)

        # check for vertical runs
        for col in range(self.boardDimension):
            for row in range(self.boardDimension):
                possibleRun = self.getRunOfTilesLengthN(n, row, col, "down")
                if not possibleRun:
                    break
                if self.noAttackInRun(possibleRun):
                    vertical.append(possibleRun)

        return horizontal, vertical

    # returns a list of Tiles with TileHitStatus.EMPTY adjacent to Tiles with TileHitStatus.HIT
    def getTilesWithNoAttackAdjacentToHits(self):
        # find tiles that have been hit
        tilesWithHits = []
        for row in range(self.boardDimension):
            for col in range(self.boardDimension):
                tile = self.getTile(row, col)
                if tile is None:
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    tilesWithHits.append(tile)
        
        # get the tiles with TileHitStatus.EMPTY adjacent to the tiles that have been hit
        tiles = []
        for tile in tilesWithHits:
            adjacentTiles = self.getAdjacentTiles(tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.getHitStatus() == TileHitStatus.EMPTY:
                    tiles.append(adjacentTile)
        list(set(tiles)) # get rid of duplicate tiles

        return tiles

    # Returns a list of horizontal hit runs and a list of vertical hit runs.
    # Runs are of length 2 or more.  Horizontal runs are ordered left to right
    # and vertical runs are ordered top to bottom.
    def getHitRuns(self):
        horizontalHitRuns = []
        verticalHitRuns = []

        # find horizontal hit runs
        for row in range(self.boardDimension):
            potentialRun = []
            for col in range(self.boardDimension):
                tile = self.getTile(row, col)
                if tile is None:
                    if potentialRun:
                        horizontalHitRuns.append(potentialRun)
                        potentialRun = []
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.getHitStatus() != TileHitStatus.HIT and potentialRun:
                    horizontalHitRuns.append(potentialRun)
                    potentialRun = []

        # find vertical hit runs
        for col in range(self.boardDimension):
            potentialRun = []
            for row in range(self.boardDimension):
                tile = self.getTile(row, col)
                if tile is None:
                    if potentialRun:
                        verticalHitRuns.append(potentialRun)
                        potentialRun = []
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.getHitStatus() != TileHitStatus.HIT and potentialRun:
                    verticalHitRuns.append(potentialRun)
                    potentialRun = []

        # get rid of any runs < length 2
        if horizontalHitRuns:
            for run in horizontalHitRuns:
                if len(run) < 2:
                    horizontalHitRuns.remove(run)
        if verticalHitRuns:
            for run in verticalHitRuns:
                if len(run) < 2:
                    verticalHitRuns.remove(run)

        return horizontalHitRuns, verticalHitRuns

    # returns a list of the tiles with TileHitStatus.EMPTY that are at 
    # the ends of hit runs
    def getTilesWithNoAttackAtEndOfHitRuns(self):
        endTiles = []
        horizontalHitRuns, verticalHitRuns = self.getHitRuns()

        for run in horizontalHitRuns:
            first = run[0]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = self.getTile(row, col - 1)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = self.getTile(row, col + 1)
            if tile:
                endTiles.append(tile)

        for run in verticalHitRuns:
            first = run[0]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = self.getTile(row - 1, col)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = self.getTile(row + 1, col)
            if tile:
                endTiles.append(tile)

        return endTiles