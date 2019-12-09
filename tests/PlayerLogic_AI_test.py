import pytest

# importing from parent directory: https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from board import Board
from player_logic import AI
from ship import ShipType

""" Testing ship placement """
# 2x2 board, placing two patrol boats.  All tiles should correspond to a ship.
def test_place_ships_1():
    board = Board(2)
    ship_type_list =[ShipType.PATROL_BOAT, ShipType.PATROL_BOAT]

    ai = AI()
    for i in range(len(ship_type_list)):
        assert ai.num_ships_placed == i
        ai.place_ship(board, ship_type_list[i])
        
    assert ai.num_ships_placed == len(ship_type_list)

    for row in range(board.get_dimension()):
        for col in range(board.get_dimension()):
            assert board.get_tile(row, col).get_ship() is not None

# 5x5 board, placing five carriers.  All tiles should correspond to a ship.
def test_place_ships_2():
    board = Board(5)
    ship_type_list =[ShipType.CARRIER, ShipType.CARRIER, ShipType.CARRIER, \
        ShipType.CARRIER, ShipType.CARRIER]

    ai = AI()
    for i in range(len(ship_type_list)):
        assert ai.num_ships_placed == i
        ai.place_ship(board, ship_type_list[i])
        
    assert ai.num_ships_placed == len(ship_type_list)

    for row in range(board.get_dimension()):
        for col in range(board.get_dimension()):
            assert board.get_tile(row, col).get_ship() is not None