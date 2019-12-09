import pytest

from game import Game, GameMode
from player import UserProfile
from view import View

from board import Board
import pickle

import unittest.mock as mock
"""
# https://stackoverflow.com/questions/46035759/making-pytest-wait-for-user-input
@pytest.yield_fixture
def fake_input():
    with mock.patch('app.my_input') as m:
        yield m

def test_my_great_func(fake_input):
    fake_input.return_value = 'y'
    assert my_great_func() == 'y'

def test_game_init(fake_input):
    game = Game(UserProfile("test"), View(), GameMode())
    fake_input.return_value = "p"
    "p"
    "t"
    "0,0"
    "s"
    "1,1"
    "s"
    "2,2"
    "s"

"""
"""
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

def test_unpickle_game():
    prof = UserProfile("jake")
    game: Game = Game.load_saved_game(prof)
    assert game.player1.user_profile.get_user_name() == "jake"
    assert game.player2.user_profile == None
    