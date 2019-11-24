from __future__ import annotations
from enum import Enum

import Ship
from Coordinate import Coordinate

# need to do "import Ship" since it has a circular import with Tile

class TileHitStatus(Enum):
    EMPTY = 1
    HIT = 2
    MISS = 3

class Tile:
    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate
        self.ship = None
        self.hitStatus = TileHitStatus.EMPTY

    def getCoordinate(self) -> Coordinate:
        return self.coordinate

    def getShip(self) -> Ship.Ship:
        return self.ship

    def getHitStatus(self) -> TileHitStatus:
        return self.hitStatus

    def setShip(self, ship: Ship.Ship):
        self.ship = ship

    def setHitStatus(self, hitStatus: TileHitStatus):
        self.hitStatus = hitStatus