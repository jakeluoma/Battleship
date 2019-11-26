import pytest

from Coordinate import Coordinate

def test_coordinate_init():
    coordinate = Coordinate(1, 1)
    assert coordinate.get_row_and_column() == (1, 1)