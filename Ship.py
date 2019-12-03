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
        self.tiles: List[Tile.Tile] = []

    def set_tiles(self, tiles: List[Tile.Tile]):
        self.tiles = tiles

    def get_size(self) -> int:
        return self.size

    def is_sunk(self) -> bool:
        sunk = True
        for tile in self.tiles:
            if tile.get_hit_status() != Tile.TileHitStatus.HIT:
                sunk = False
                break
        return sunk

class ShipType(Enum):
    PATROL_BOAT = 0
    SUBMARINE = 1
    DESTROYER = 2
    BATTLESHIP = 3
    CARRIER = 4

# Usage: call startShip(), then placeShip(), then returnCompletedShip() to get a Ship object.
# Can call getShipSize() at any time
class ShipBuilder:
    def __init__(self):
        self.ship = None
        self.finished = False

    def start_ship(self, ship_type: ShipType):
        self.finished = False

        if ship_type == ShipType.PATROL_BOAT:
            self.ship = Ship(ship_type.name, 2)
        if ship_type == ShipType.SUBMARINE:
            self.ship = Ship(ship_type.name, 3)
        if ship_type == ShipType.DESTROYER:
            self.ship = Ship(ship_type.name, 3)
        if ship_type == ShipType.BATTLESHIP:
            self.ship = Ship(ship_type.name, 4)
        if ship_type == ShipType.CARRIER:
            self.ship = Ship(ship_type.name, 5)

    def place_ship(self, tiles: List[Tile.Tile]):
        if self.ship is not None:
            if len(tiles) != self.get_ship_size():
                print("Length of tiles given for ship placement doesn't match ship length!")
            self.finished = True
            self.ship.set_tiles(tiles)
            for tile in tiles:
                tile.set_ship(self.ship)

    def return_completed_ship(self) -> Ship:
        if self.finished == True:
            return self.ship
        else:
            return None

    def get_ship_size(self) -> int:
        if self.ship is not None:
            return self.ship.get_size()
        else:
            return 0