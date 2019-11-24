import pytest

from Coordinate import Coordinate
import Tile
import Ship

def test_tile_init():
    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)

    assert tile.getCoordinate() == coordinate
    assert tile.getShip() == None
    assert tile.getHitStatus() == Tile.TileHitStatus.EMPTY

def test_tile_ship_functions():
    ship = Ship.Ship("test", 1)

    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)
    tile.setShip(ship)

    assert tile.getShip() == ship

def test_tile_hit_functions():
    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)

    tile.setHitStatus(Tile.TileHitStatus.HIT)
    assert tile.getHitStatus() == Tile.TileHitStatus.HIT

    tile.setHitStatus(Tile.TileHitStatus.MISS)
    assert tile.getHitStatus() == Tile.TileHitStatus.MISS