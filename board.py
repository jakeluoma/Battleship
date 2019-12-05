from Tile import *
from Coordinate import Coordinate

from typing import List
from typing import Tuple


class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


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


class BoardHelper:
    """ General Helper Functions """

    # returns a run of tiles of length n, given a starting row, column, and direction.  If no
    # run meets that criteria or if an invalid direction is given, returns an empty list.
    # Note that runs are always ordered left to right or up to down.
    @staticmethod
    def get_run_of_tiles_length_n(board: Board, n: int, row: int, col: int, direction: Direction) -> List[Tile]:
        run: List[Tile] = []
        if direction == direction.right:
            possibleRun: List[Tile] = []
            for i in range(n):
                colIndex = col + i
                tile = board.get_tile(row, colIndex)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == direction.left:
            possibleRun: List[Tile] = []
            for i in range(n):
                colIndex = col - i
                tile = board.get_tile(row, colIndex)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun
        elif direction == direction.down:
            possibleRun: List[Tile] = []
            for i in range(n):
                rowIndex = row + i
                tile = board.get_tile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.append(tile)
            run = possibleRun
        elif direction == direction.up:
            possibleRun: List[Tile] = []
            for i in range(n):
                rowIndex = row - i
                tile = board.get_tile(rowIndex, col)
                if tile is None:
                    break
                possibleRun.insert(0, tile)
            run = possibleRun

        return run

    @staticmethod
    def get_run_of_tiles_length_n_with_no_ship(board: Board, n: int, row: int, col: int,
                                               direction: Direction) -> List[Tile]:
        run: List[Tile] = BoardHelper.get_run_of_tiles_length_n(board, n, row, col,
                                                    direction)
        if board.ship_in_run(run):
            run = []

        return run

    # gets tiles adjacent to the given tile.  Will only return tiles that
    # are within the board.
    @staticmethod
    def get_adjacent_tiles(board: Board, tile: Tile) -> List[Tile]:
        ret: List[Tile] = []
        locations = List[Tuple[int, int]]
        row, col = tile.getRowAndColumn()
        locations.append((row + 1, col))
        locations.append((row - 1, col))
        locations.append((row, col + 1))
        locations.append((row, col - 1))

        for location in locations:
            tile = board.get_tile(*location)
            if tile is not None:
                ret.append(tile)

        return ret

    """ Ship Placement Helper Functions """

    # returns a list of runs of tiles of length n.  No tile in a run contains a ship.
    # the list contains both horizontal and vertical runs.
    @staticmethod
    def get_runs_of_tiles_with_no_ship_length_n(board: Board, n: int) -> List[List[Tile]]:
        ret: List[List[Tile]] = []

        # check for horizontal runs
        for row in range(board.get_dimension()):
            for col in range(board.get_dimension()):
                possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.right)
                if not possibleRun:
                    break
                ret.append(possibleRun)

        # check for vertical runs
        for col in range(board.get_dimension()):
            for row in range(board.get_dimension()):
                possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.down)
                if not possibleRun:
                    break
                ret.append(possibleRun)

        return ret

    # returns a list of runs of tiles of length n.  It contains both horizontal and vertical runs.  None
    # of the tiles in a given run contain a ship.  The runs must have at least one
    # tile adjacent to a tile that already contains a ship.
    @staticmethod
    def get_runs_of_tiles_with_no_ship_length_n_next_to_ship(board: Board, n: int) -> List[List[Tile]]:
        # find tiles that already have ships
        tilesWithShips: List[Tile] = []
        for row in range(board.get_dimension()):
            for col in range(board.get_dimension()):
                tile = board.get_tile(row, col)
                if tile is None:
                    continue
                if tile.get_ship() is not None:
                    tilesWithShips.append(tile)

        # starting tiles are tiles without ships adjacent to the tiles that have ships
        startingTiles: List[Tile] = []
        for tile in tilesWithShips:
            adjacentTiles = BoardHelper.get_adjacent_tiles(board, tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.get_ship() is None:
                    startingTiles.append(adjacentTile)
        list(set(startingTiles))  # get rid of duplicate tiles

        # from each starting tile, try to get a run of length N in each direction
        ret: List[List[Tile]] = []
        for tile in startingTiles:
            row, col = tile.get_coordinate().get_row_and_column()

            possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.up)
            if possibleRun:
                ret.append(possibleRun)

            possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.down)
            if possibleRun:
                ret.append(possibleRun)

            possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.right)
            if possibleRun:
                ret.append(possibleRun)

            possibleRun = BoardHelper.get_run_of_tiles_length_n_with_no_ship(board, n, row, col, Direction.left)
            if possibleRun:
                ret.append(possibleRun)

        # only want unique runs
        # https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
        ret: List[List[Tile]] = [list(x) for x in set(tuple(x) for x in ret)]

        return ret

    """ Attack Selection Helper Functions """

    # returns a list of runs of tiles of length n.  None
    # of the tiles in a given run have been attacked yet.
    @staticmethod
    def get_runs_of_tiles_with_no_attack_length_n(board: Board, n: int) -> List[List[Tile]]:
        ret: List[List[Tile]] = []

        # check for horizontal runs
        for row in range(board.get_dimension()):
            for col in range(board.get_dimension()):
                possibleRun = BoardHelper.get_run_of_tiles_length_n(board, n, row, col, Direction.right)
                if not possibleRun:
                    break
                if not board.attack_in_run(possibleRun):
                    ret.append(possibleRun)

        # check for vertical runs
        for col in range(board.get_dimension()):
            for row in range(board.get_dimension()):
                possibleRun = BoardHelper.get_run_of_tiles_length_n(board, n, row, col, Direction.down)
                if not possibleRun:
                    break
                if not board.attack_in_run(possibleRun):
                    ret.append(possibleRun)

        return ret

    # returns a list of Tiles with TileHitStatus.EMPTY adjacent to Tiles with TileHitStatus.HIT
    @staticmethod
    def get_tiles_with_no_attack_adjacent_to_hits(board: Board) -> List[Tile]:
        # find tiles that have been hit
        tilesWithHits: List[Tile] = []
        for row in range(board.get_dimension()):
            for col in range(board.get_dimension()):
                tile = board.get_tile(row, col)
                if tile is None:
                    continue
                if tile.get_hit_status() == TileHitStatus.HIT:
                    tilesWithHits.append(tile)

        # get the tiles with TileHitStatus.EMPTY adjacent to the tiles that have been hit
        tiles: List[Tile] = []
        for tile in tilesWithHits:
            adjacentTiles = BoardHelper.get_adjacent_tiles(board, tile)
            for adjacentTile in adjacentTiles:
                if adjacentTile.get_hit_status() == TileHitStatus.EMPTY:
                    tiles.append(adjacentTile)
        list(set(tiles))  # get rid of duplicate tiles

        return tiles

    # Returns a list of horizontal hit runs and a list of vertical hit runs.
    # Runs are of length 2 or more.  Horizontal runs are ordered left to right
    # and vertical runs are ordered top to bottom.
    @staticmethod
    def get_hit_runs(board: Board) -> Tuple[List[List[Tile]], List[List[Tile]]]:
        horizontalHitRuns: List[List[Tile]] = []
        verticalHitRuns: List[List[Tile]] = []

        # find horizontal hit runs
        for row in range(board.get_dimension()):
            potentialRun: List[Tile] = []
            for col in range(board.get_dimension()):
                tile = board.get_tile(row, col)
                if tile is None:
                    if potentialRun:
                        horizontalHitRuns.append(potentialRun)
                        potentialRun: List[Tile] = []
                    continue
                if tile.get_hit_status() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.get_hit_status() != TileHitStatus.HIT and potentialRun:
                    horizontalHitRuns.append(potentialRun)
                    potentialRun: List[Tile] = []

        # find vertical hit runs
        for col in range(board.get_dimension()):
            potentialRun: List[Tile] = []
            for row in range(board.get_dimension()):
                tile = board.get_tile(row, col)
                if tile is None:
                    if potentialRun:
                        verticalHitRuns.append(potentialRun)
                        potentialRun: List[Tile] = []
                    continue
                if tile.get_hit_status() == TileHitStatus.HIT:
                    potentialRun.append(tile)
                if tile.get_hit_status() != TileHitStatus.HIT and potentialRun:
                    verticalHitRuns.append(potentialRun)
                    potentialRun: List[Tile] = []

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
    def get_tiles_with_no_attack_at_end_of_hit_runs(board: Board):
        endTiles: List[Tile] = []
        horizontalHitRuns, verticalHitRuns = BoardHelper.get_hit_runs(board)

        for run in horizontalHitRuns:
            first = run[0]
            row, col = first.get_coordinate().get_row_and_column()
            tile = board.get_tile(row, col - 1)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.get_coordinate().get_row_and_column()
            tile = board.get_tile(row, col + 1)
            if tile:
                endTiles.append(tile)

        for run in verticalHitRuns:
            first = run[0]
            row, col = first.get_coordinate().get_row_and_column()
            tile = board.get_tile(row - 1, col)
            if tile:
                endTiles.append(tile)

            last = run[-1]
            row, col = first.get_coordinate().get_row_and_column()
            tile = board.get_tile(row + 1, col)
            if tile:
                endTiles.append(tile)

        return endTiles