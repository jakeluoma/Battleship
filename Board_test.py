import pytest

from Board import Board
from Coordinate import Coordinate
import Ship
import Tile

def test_board_init():
    dimension = 10
    board = Board(dimension)

    assert dimension == board.getDimension()
    assert len(board.boardTiles) == dimension
    for i in range(dimension):
        assert len(board.boardTiles[i]) == dimension

    for row in range(dimension):
        for col in range(dimension):
            tile = board.getTile(row, col)
            assert tile != None
            coordinate = tile.getCoordinate()
            assert coordinate != None
            assert coordinate.getRowAndColumn() == (row, col)

def test_processIncomingAttack():
    dimension = 2
    board = Board(dimension)

    ship = Ship.Ship("test", 1)
    tile = board.getTile(0, 0)
    tile.setShip(ship)

    tiles = []
    tiles.append(tile)
    ship.setTiles(tiles)

    hit = Coordinate(0, 0)
    miss = Coordinate(0, 1)
    another_miss = Coordinate(1, 0)

    coordinates = []
    coordinates.append(hit)
    coordinates.append(miss)
    coordinates.append(another_miss)

    hits, misses = board.processIncomingAttack(coordinates)

    assert len(hits) == 1
    assert hit in hits
    assert len(misses) == 2
    assert miss in misses
    assert another_miss in misses

    assert ship.isSunk() == True

def test_updateHitsAndMisses():
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

    board.updateHitsAndMisses(hits, misses)
    assert board.getTile(0, 0).getHitStatus() == Tile.TileHitStatus.HIT
    assert board.getTile(1, 0).getHitStatus() == Tile.TileHitStatus.HIT
    assert board.getTile(0, 1).getHitStatus() == Tile.TileHitStatus.MISS
    assert board.getTile(1, 1).getHitStatus() == Tile.TileHitStatus.EMPTY