import pytest

from game import Game, GameMode
from player import UserProfile

from board import Board
import pickle

# will fail until we can actually get a game set up by getting user input

"""
def test_game_init():
    game = Game(UserProfile("jake"), GameMode())


def test_game_save_and_load():
    game = Game(UserProfile("jake"), GameMode())
    game.save_game()
    loaded_game = Game.load_saved_game()
    assert game == loaded_game

"""

"""
def test_trying_pickle():
    dimension = 10
    board = Board(dimension)
    file_name = "test.p"

    pickle.dump(board, open(file_name, "wb"))

    loaded_board: Board = pickle.load(open(file_name, "rb"))

    assert loaded_board.get_dimension() == board.get_dimension()
"""