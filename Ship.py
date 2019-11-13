from abc import ABC
from Tile import *

# for now, no special attacks.  Let's just get the program working first.
class Ship:
    def __init__(self, name, size, tiles):
        if size != len(tiles):
            print("Size of ship " + name + " is " + size + " but it was assigned " + len(tiles) + " tiles")

        self.name = name
        self.size = size
        self.tiles = tiles

    def isSunk(self):
        sunk = True
        for tile in self.tiles:
            if tile.getHitStatus != TileHitStatus.HIT:
                sunk = False
                break
        return sunk


class ShipType(Enum):
    patrol_board = 0
    submarine = 1
    destroyer = 2
    battelship = 3
    carrier = 4


class ShipFactory:
    pass