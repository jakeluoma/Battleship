from abc import ABC
from enum import Enum
from typing import List
from typing import Tuple
from random import randrange

from Board import Board
from Coordinate import Coordinate
from Ship import ShipBuilder, Ship, ShipType
from Tile import Tile, TileHitStatus

class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3

class BoardHelper:
    """ General Helper Functions """

    # returns a run of tiles of length n, given a starting row, column, and direction.  If no
    # run meets that criteria or if an invalid direction is given, returns an empty list.
    # Note that runs are always ordered left to right or up to down.
    @staticmethod
    def getRunOfTilesLengthN(board: Board, n: int, row: int, col: int, direction: Direction) -> List[Tile]:
        run = []
        if direction == direction.right:
            possibleRun = []
            for i in range(n):
                colIndex = col + i
                tile = board.getTile(row, colIndex)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == direction.left:
            possibleRun = []
            for i in range(n):
                colIndex = col - i
                tile = board.getTile(row, colIndex)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun
        elif direction == direction.down:
            possibleRun = []
            for i in range(n):
                rowIndex = row + i
                tile = board.getTile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == direction.up:
            possibleRun = []
            for i in range(n):
                rowIndex = row - i
                tile = board.getTile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun

        return run

    # @staticmethod
    
    # gets tiles adjacent to the given tile.  Will only return tiles that
    # are within the board.
    @staticmethod
    def getAdjacentTiles(board: Board, tile: Tile) -> List[Tile]:
        ret = List[Tile]
        locations = List[Tuple[int, int]]
        row, col = tile.getRowAndColumn()
        locations.append((row + 1, col))
        locations.append((row - 1, col))
        locations.append((row, col + 1))
        locations.append((row, col - 1))

        for location in locations:
            tile = board.getTile(*location)
            if tile is not None:
                ret.append(tile)

        return ret

    """ Ship Placement Helper Functions """

    # returns a list of runs of tiles of length n.  No tile in a run contains a ship.
    # the list contains both horizontal and vertical runs.
    @staticmethod
    def getRunsOfTilesWithNoShipLengthN(board: Board, n: int) -> List[List[Tile]]:
        ret = List[List[Tile]]

        # check for horizontal runs
        for row in range(board.getDimension()):
            for col in range(board.getDimension()):
                possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.right)
                if not possibleRun:
                    break
                if not board.shipInRun(possibleRun):
                    ret.append(possibleRun)

        # check for vertical runs
        for col in range(board.getDimension()):
            for row in range(board.getDimension()):
                possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.down)
                if not possibleRun:
                    break
                if not board.shipInRun(possibleRun):
                    ret.append(possibleRun)

        return ret

    # returns a list of runs of tiles of length n.  It contains both horizontal and vertical runs.  None
    # of the tiles in a given run contain a ship.  The runs must have at least one
    # tile adjacent to a tile that already contains a ship.
    @staticmethod
    def getRunsOfTilesWithNoShipLengthNNextToShip(board: Board, n: int) -> List[List[Tile]]:
        # find tiles that already have ships
        tilesWithShips = List[Tile]
        for row in range(board.getDimension()):
            for col in range(board.getDimension()):
                tile = board.getTile(row, col)
                if tile is None:
                    continue
                if tile.getShip() is not None:
                    tilesWithShips.append(tile)

        # starting tiles are tiles without ships adjacent to the tiles that have ships
        startingTiles = List[Tile]
        for tile in tilesWithShips:
            adjacentTiles = board.getAdjacentTiles(tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.getShip() is None:
                    startingTiles.append(adjacentTile)
        list(set(startingTiles))  # get rid of duplicate tiles

        # from each starting tile, try to get a run of length N in each direction
        ret = List[List[Tile]]
        for tile in startingTiles:
            row, col = tile.getCoordinate().getRowAndColumn()

            possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.up)
            if possibleRun:
                if BoardHelper.noShipInRun(possibleRun):
                    ret.append(possibleRun)

            possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.down)
            if possibleRun:
                if BoardHelper.noShipInRun(possibleRun):
                    ret.append(possibleRun)

            possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.right)
            if possibleRun:
                if BoardHelper.noShipInRun(possibleRun):
                    ret.append(possibleRun)

            possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.left)
            if possibleRun:
                if BoardHelper.noShipInRun(possibleRun):
                    ret.append(possibleRun)

        # only want unique runs
        # https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
        ret = [list(x) for x in set(tuple(x) for x in ret)]

        return ret

    """ Attack Selection Helper Functions """

    # returns a list of runs of tiles of length n.  None
    # of the tiles in a given run have been attacked yet.
    @staticmethod
    def getRunsOfTilesWithNoAttackLengthN(board: Board, n: int) -> List[List[Tile]]:
        ret = List[List[Tile]]

        # check for horizontal runs
        for row in range(board.getDimension()):
            for col in range(board.getDimension()):
                possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.right)
                if not possibleRun:
                    break
                if not BoardHelper.attackInRun(possibleRun):
                    ret.append(possibleRun)

        # check for vertical runs
        for col in range(board.getDimension()):
            for row in range(board.getDimension()):
                possibleRun = BoardHelper.getRunOfTilesLengthN(board, n, row, col, Direction.down)
                if not possibleRun:
                    break
                if not BoardHelper.attackInRun(possibleRun):
                    ret.append(possibleRun)

        return ret

    # returns a list of Tiles with TileHitStatus.EMPTY adjacent to Tiles with TileHitStatus.HIT
    @staticmethod
    def getTilesWithNoAttackAdjacentToHits(board: Board) -> List[Tile]:
        # find tiles that have been hit
        tilesWithHits = List[Tile]
        for row in range(board.getDimension()):
            for col in range(board.getDimension()):
                tile = board.getTile(row, col)
                if tile is None:
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    tilesWithHits.append(tile)

        # get the tiles with TileHitStatus.EMPTY adjacent to the tiles that have been hit
        tiles = List[Tile]
        for tile in tilesWithHits:
            adjacentTiles = BoardHelper.getAdjacentTiles(board, tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.getHitStatus() == TileHitStatus.EMPTY:
                    tiles.append(adjacentTile)
        list(set(tiles))  # get rid of duplicate tiles

        return tiles

    # Returns a list of horizontal hit runs and a list of vertical hit runs.
    # Runs are of length 2 or more.  Horizontal runs are ordered left to right
    # and vertical runs are ordered top to bottom.
    @staticmethod
    def getHitRuns(board: Board) -> Tuple[List[List[Tile]], List[List[Tile]]]:
        horizontalHitRuns = List[List[Tile]]
        verticalHitRuns = List[List[Tile]]

        # find horizontal hit runs
        for row in range(board.getDimension()):
            potentialRun = List[Tile]
            for col in range(board.getDimension()):
                tile = board.getTile(row, col)
                if tile is None:
                    if potentialRun:
                        horizontalHitRuns.append(potentialRun)
                        potentialRun = List[Tile]
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.getHitStatus() != TileHitStatus.HIT and potentialRun:
                    horizontalHitRuns.append(potentialRun)
                    potentialRun = List[Tile]

        # find vertical hit runs
        for col in range(board.getDimension()):
            potentialRun = List[Tile]
            for row in range(board.getDimension()):
                tile = board.getTile(row, col)
                if tile is None:
                    if potentialRun:
                        verticalHitRuns.append(potentialRun)
                        potentialRun = List[Tile]
                    continue
                if tile.getHitStatus() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.getHitStatus() != TileHitStatus.HIT and potentialRun:
                    verticalHitRuns.append(potentialRun)
                    potentialRun = List[Tile]

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
    @staticmethod
    def getTilesWithNoAttackAtEndOfHitRuns(board: Board):
        endTiles = List[Tile]
        horizontalHitRuns, verticalHitRuns = BoardHelper.getHitRuns(board)

        for run in horizontalHitRuns:
            first = run[0]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = board.getTile(row, col - 1)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = board.getTile(row, col + 1)
            if tile:
                endTiles.append(tile)

        for run in verticalHitRuns:
            first = run[0]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = board.getTile(row - 1, col)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.getCoordinate().getRowAndColumn()
            tile = board.getTile(row + 1, col)
            if tile:
                endTiles.append(tile)

        return endTiles


class PlayerLogic(ABC):
    def __init__(self):
        self.ship_builder = ShipBuilder()

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
        self.ship_builder.startShip(ship_type)

        runs = List[List[Tile]]
        if self.num_ships_placed == 0: # place ship anywhere
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthN(board, self.ship_builder.getShipSize())
        elif randrange(0, 3) == 0: # maybe place ship next to an already placed ship
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthNNextToShip(board, self.ship_builder.getShipSize())
        else: # place ship anywhere
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthN(board, self.ship_builder.getShipSize())

        # Get initial coordinate and direction from shell
        if self.num_ships_placed == 0:
            possibleRun = BoardHelper.getRunOfTilesLengthN(board, self.ship_builder.getShipSize(), row, col, direction)
            if not possibleRun:
                break
            if not board.shipInRun(possibleRun):
                ret.append(possibleRun)

        if len(runs) == 0:
            print("Impossible to place ship " + ship_type.name)
            return None
        index = randrange(0, len(runs)) # pick where to place ship among valid places
        run = runs[index]
        self.ship_builder.placeShip(run)
        self.num_ships_placed += 1
        return self.ship_builder.returnCompletedShip()


    def select_attack(self, target_board: Board) -> Coordinate:
        """
        similar to place_ship()... just make the right canvas, give to view, call self.view.getCoordinate(),
        check with board via board.getTile(coordinate) that it's a valid coordinate before returning it.
        """
        pass


""" AI Control """
class AI(PlayerLogic):
    def __init__(self):
        super()
        self.num_ships_placed = 0

    # Places a ship onto the board
    def place_ship(self, board: Board, ship_type: ShipType) -> Ship:
        self.ship_builder.startShip(ship_type)

        runs = List[List[Tile]]
        if self.num_ships_placed == 0: # place ship anywhere
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthN(board, self.ship_builder.getShipSize())
        elif randrange(0, 3) == 0: # maybe place ship next to an already placed ship
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthNNextToShip(board, self.ship_builder.getShipSize())
        else: # place ship anywhere
            runs = BoardHelper.getRunsOfTilesWithNoShipLengthN(board, self.ship_builder.getShipSize())

        if len(runs) == 0:
            print("Impossible to place ship " + ship_type.name)
            return None
        index = randrange(0, len(runs)) # pick where to place ship among valid places
        run = runs[index]
        self.ship_builder.placeShip(run)
        self.num_ships_placed += 1
        return self.ship_builder.returnCompletedShip()

    # choose where to attack and return that Coordinate
    def select_attack(self, target_board: Board) -> Coordinate:
        potentialTargetTiles = List[Tile]

        # always attack ends of hit runs if there are any
        potentialTargetTiles = BoardHelper.getTilesWithNoAttackAtEndOfHitRuns(target_board)
        if potentialTargetTiles:
            index = randrange(0, len(potentialTargetTiles))
            return potentialTargetTiles[index].getCoordinate()

        # choose whether to attack tiles adjacent to hits, if there are any, or attack randomly
        if randrange(0, 4) < 3:
            # attack tiles adjacent to hits if there are any
            potentialTargetTiles = BoardHelper.getTilesWithNoAttackAdjacentToHits(target_board)
            if potentialTargetTiles:
                index = randrange(0, len(potentialTargetTiles))
                return potentialTargetTiles[index].getCoordinate()

        # attack randomly
        n = 2 # hardcoded to length of patrol boat for now
        potentialTargetTiles = BoardHelper.getRunsOfTilesWithNoAttackLengthN(target_board, n)
        index = randrange(0, len(potentialTargetTiles))
        return potentialTargetTiles[index][n-1].getCoordinate()