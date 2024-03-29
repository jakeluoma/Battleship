from __future__ import annotations

from enum import Enum
from typing import List, Optional

# need to do "import Tile" since it has a circular import with Ship
from components.tile import Tile, TileHitStatus


class Ship:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size
        self.tiles: List[Tile] = []

    def set_tiles(self, tiles: List[Tile]):
        self.tiles = tiles

    def get_size(self) -> int:
        return self.size

    def is_sunk(self) -> bool:
        sunk = True
        for tile in self.tiles:
            if tile.get_hit_status() != TileHitStatus.HIT:
                sunk = False
                break
        return sunk


class ShipType(Enum):
    PATROL_BOAT = 0
    SUBMARINE = 1
    DESTROYER = 2
    BATTLESHIP = 3
    CARRIER = 4


ship_size_map = {
    ShipType.PATROL_BOAT: 2,
    ShipType.SUBMARINE: 3,
    ShipType.DESTROYER: 3,
    ShipType.BATTLESHIP: 4,
    ShipType.CARRIER: 5
}


# Usage: call startShip(), then placeShip(), then returnCompletedShip() to get a Ship object.
# Can call getShipSize() at any time
# Implements the Builder pattern along with PlayerLogic
class ShipBuilder:
    def __init__(self):
        self.ship = None
        self.finished = False

    def start_ship(self, ship_type: ShipType):
        self.finished = False
        self.ship = Ship(ship_type.name, ship_size_map[ship_type])

    def place_ship(self, tiles: List[Tile]):
        if self.ship is not None:
            if len(tiles) != self.get_ship_size():
                print("Length of tiles given for ship placement doesn't match ship length!:"
                      " Tiles {} Ship size: {}".format(len(tiles), self.ship.get_size()))
            self.finished = True
            self.ship.set_tiles(tiles)
            for tile in tiles:
                tile.set_ship(self.ship)

    def return_completed_ship(self) -> Optional[Ship]:
        if self.finished == True:
            return self.ship
        else:
            return None

    def get_ship_size(self) -> int:
        if self.ship is not None:
            return self.ship.get_size()
        else:
            return 0
