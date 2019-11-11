from enum import Enum

class TileHitStatus(Enum):
    EMPTY = 1
    HIT = 2
    MISS = 3

class Tile:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.ship = None
        self.hitStatus = TileHitStatus.EMPTY

    def getCoordinate(self):
        return self.coordinate

    def getShip(self):
        return self.ship

    def getHitStatus(self):
        return self.hitStatus

    def setShip(self, ship):
        self.ship = ship

    def setHitStatus(self, hitStatus):
        self.hitStatus = hitStatus