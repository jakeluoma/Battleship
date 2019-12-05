import pytest

from board import Board
from PlayerLogic import AI
from Ship import ShipType

def test_place_ships_1():
    board = Board(2)
    ship_type_list =[ShipType.PATROL_BOAT, ShipType.PATROL_BOAT]

    ai = AI()
    ai.place_ship(board, ship_type_list[0])
    assert ai.num_ships_placed == 1

    ai.place_ship(board, ship_type_list[1])
    assert ai.num_ships_placed == 2

    for row in range(board.get_dimension()):
        for col in range(board.get_dimension()):
            assert board.get_tile(row, col).get_ship() is not None