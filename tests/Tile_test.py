import pytest

# importing from parent directory: https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

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