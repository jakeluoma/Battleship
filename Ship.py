from __future__ import annotations
from abc import ABC
from enum import Enum

from typing import List

import Tile

# need to do "import Tile" since it has a circular import with Ship

# for now, no special attacks.  Let's just get the program working first.
class Ship:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.tiles = List[Tile.Tile]

    def setTiles(self, tiles: List[Tile.Tile]):
        self.tiles = tiles

    def getSize(self) -> int:
        return self.size

    def isSunk(self) -> bool:
        sunk = True
        for tile in self.tiles:
            if tile.getHitStatus() != Tile.TileHitStatus.HIT:
                sunk = False
                break
        return sunk

class ShipType(Enum):
    patrol_boat = 0
    submarine = 1
    destroyer = 2
    battleship = 3
    carrier = 4

# Usage: call startShip(), then placeShip(), then returnCompletedShip() to get a Ship object.
# Can call getShipSize() at any time
class ShipBuilder:
    def __init__(self):
        self.ship = None
        self.finished = False

    def startShip(self, ship_type: ShipType):
        self.finished = False

        if ship_type == ShipType.patrol_boat:
            self.ship = Ship(ship_type.name, 2)
        if ship_type == ShipType.submarine:
            self.ship = Ship(ship_type.name, 3)
        if ship_type == ShipType.destroyer:
            self.ship = Ship(ship_type.name, 3)
        if ship_type == ShipType.battleship:
            self.ship = Ship(ship_type.name, 4)
        if ship_type == ShipType.carrier:
            self.ship = Ship(ship_type.name, 5)

    def placeShip(self, tiles: List[Tile.Tile]):
        if self.ship is not None:
            self.finished = True
            self.ship.setTiles(tiles)
            for tile in tiles:
                tile.setShip(ship)

    def returnCompletedShip(self) -> Ship:
        if self.finished == True:
            return self.ship

    def getShipSize(self) -> int:
        if self.ship is not None:
            return self.ship.getSize()
        else:
            return 0