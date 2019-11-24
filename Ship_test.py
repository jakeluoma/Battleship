import pytest

from Coordinate import Coordinate
import Ship
import Tile

def test_ship_init_and_isSunk():
    ship = Ship.Ship("test", 1)
    coordinate = Coordinate(0, 0)
    tile = Tile.Tile(coordinate)

    tile.setShip(ship)

    tiles = []
    tiles.append(tile)
    ship.setTiles(tiles)

    assert ship.getSize() == 1
    assert ship.isSunk() == False

    tile.setHitStatus(Tile.TileHitStatus.HIT)
    assert ship.isSunk() == True

def test_shipBuilder():
    ship_builder = Ship.ShipBuilder()
    ship_builder.startShip(Ship.ShipType.BATTLESHIP)
    assert ship_builder.getShipSize() == 4
    assert ship_builder.returnCompletedShip() == None

    tiles = []
    for i in range(4):
        coordinate = Coordinate(0, i)
        tiles.append(Tile.Tile(coordinate))

    ship_builder.placeShip(tiles)
    ship = ship_builder.returnCompletedShip()

    assert len(ship.tiles) == 4
    for tile in ship.tiles:
        assert tile.getShip() == ship
        
    for tile in tiles:
        assert tile.getShip() == ship