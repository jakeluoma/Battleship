import pytest

# importing from parent directory: https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from board import Board, BoardHelper
from Coordinate import Coordinate
import Ship
import Tile

def test_board_init():
    dimension = 10
    board = Board(dimension)

    assert dimension == board.get_dimension()
    assert len(board.boardTiles) == dimension
    for i in range(dimension):
        assert len(board.boardTiles[i]) == dimension

    for row in range(dimension):
        for col in range(dimension):
            tile = board.get_tile(row, col)
            assert tile != None
            coordinate = tile.get_coordinate()
            assert coordinate != None
            assert coordinate.get_row_and_column() == (row, col)

def test_process_incoming_attack():
    dimension = 2
    board = Board(dimension)

    ship = Ship.Ship("test", 1)
    tile = board.get_tile(0, 0)
    tile.set_ship(ship)

    tiles = []
    tiles.append(tile)
    ship.set_tiles(tiles)

    hit = Coordinate(0, 0)
    miss = Coordinate(0, 1)
    another_miss = Coordinate(1, 0)

    coordinates = []
    coordinates.append(hit)
    coordinates.append(miss)
    coordinates.append(another_miss)

    hits, misses = board.process_incoming_attack(coordinates)

    assert len(hits) == 1
    assert hit in hits
    assert len(misses) == 2
    assert miss in misses
    assert another_miss in misses

    assert ship.is_sunk() == True

def test_update_hits_and_misses():
    dimension = 2
    board = Board(dimension)

    hit = Coordinate(0, 0)
    another_hit = Coordinate(1, 0)
    miss = Coordinate(0, 1)

    hits = []
    hits.append(hit)
    hits.append(another_hit)

    misses = []
    misses.append(miss)

    board.update_hits_and_misses(hits, misses)
    assert board.get_tile(0, 0).get_hit_status() == Tile.TileHitStatus.HIT
    assert board.get_tile(1, 0).get_hit_status() == Tile.TileHitStatus.HIT
    assert board.get_tile(0, 1).get_hit_status() == Tile.TileHitStatus.MISS
    assert board.get_tile(1, 1).get_hit_status() == Tile.TileHitStatus.EMPTY

def test_get_hit_runs():
    dimension = 3
    board = Board(dimension)
    
    board.get_tile(0,0).set_hit_status(Tile.TileHitStatus.HIT)
    board.get_tile(0,1).set_hit_status(Tile.TileHitStatus.HIT)
    board.get_tile(1,0).set_hit_status(Tile.TileHitStatus.HIT)

    horizontal, vertical = BoardHelper.get_hit_runs(board)

    assert len(horizontal) == 1
    assert len(vertical) == 1

    horizontal_run = horizontal[0]
    assert len(horizontal_run) == 2
    assert horizontal_run[0] == board.get_tile(0,0)
    assert horizontal_run[1] == board.get_tile(0,1)

    vertical_run = vertical[0]
    assert len(vertical_run) == 2
    assert vertical_run[0] == board.get_tile(0,0)
    assert vertical_run[1] == board.get_tile(1,0)

def test_get_tiles_with_no_attack_at_end_of_hit_runs():
    dimension = 3
    board = Board(dimension)
    
    board.get_tile(0,0).set_hit_status(Tile.TileHitStatus.HIT)
    board.get_tile(0,1).set_hit_status(Tile.TileHitStatus.HIT)
    board.get_tile(1,0).set_hit_status(Tile.TileHitStatus.HIT)

    tiles = BoardHelper.get_tiles_with_no_attack_at_end_of_hit_runs(board)
    assert len(tiles) == 2
    assert board.get_tile(0,2) in tiles
    assert board.get_tile(2,0) in tiles
