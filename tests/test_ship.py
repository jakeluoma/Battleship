# importing from parent directory: https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from components.tile import Coordinate
import Tile

def test_ship_init_and_is_sunk():
    ship = ship.Ship("test", 1)
    coordinate = Coordinate(0, 0)
    tile = Tile.Tile(coordinate)

    tile.set_ship(ship)

    tiles = []
    tiles.append(tile)
    ship.set_tiles(tiles)

    assert ship.get_size() == 1
    assert ship.is_sunk() == False

    tile.set_hit_status(Tile.TileHitStatus.HIT)
    assert ship.is_sunk() == True

def test_shipBuilder():
    ship_builder = ship.ShipBuilder()
    ship_builder.start_ship(ship.ShipType.BATTLESHIP)
    assert ship_builder.get_ship_size() == 4
    assert ship_builder.return_completed_ship() == None

    tiles = []
    for i in range(4):
        coordinate = Coordinate(0, i)
        tiles.append(Tile.Tile(coordinate))

    ship_builder.place_ship(tiles)
    ship = ship_builder.return_completed_ship()

    assert len(ship.tiles) == 4
    for tile in ship.tiles:
        assert tile.get_ship() == ship
        
    for tile in tiles:
        assert tile.get_ship() == ship