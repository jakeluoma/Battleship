import pytest

from Coordinate import Coordinate
import Tile
import Ship

def test_tile_init():
    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)

    assert tile.get_coordinate() == coordinate
    assert tile.get_ship() == None
    assert tile.get_hit_status() == Tile.TileHitStatus.EMPTY

def test_tile_ship_functions():
    ship = Ship.Ship("test", 1)

    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)
    tile.set_ship(ship)

    assert tile.get_ship() == ship

def test_tile_hit_functions():
    coordinate = Coordinate(1, 1)
    tile = Tile.Tile(coordinate)

    tile.set_hit_status(Tile.TileHitStatus.HIT)
    assert tile.get_hit_status() == Tile.TileHitStatus.HIT

    tile.set_hit_status(Tile.TileHitStatus.MISS)
    assert tile.get_hit_status() == Tile.TileHitStatus.MISS