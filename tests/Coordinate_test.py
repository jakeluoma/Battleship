import pytest

# importing from parent directory: https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from coordinate import Coordinate

def test_coordinate_init():
    coordinate = Coordinate(1, 1)
    assert coordinate.get_row_and_column() == (1, 1)