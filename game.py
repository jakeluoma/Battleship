from abc import ABC
from typing import List

from Board import Board
from Coordinate import Coordinates
from Ship import ShipType, Ship, ShipFactory


class Game:
    player = None
    opponent = None
    player_board = None
    opponent_board = None

    def __init__(self):
        pass

    def create_board(self, board_dimensions):
        return Board(board_dimensions)

    def run_game(self):
        pass


