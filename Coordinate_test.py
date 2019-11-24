import pytest

from Coordinate import Coordinate

def test_coordinate_init():
    coordinate = Coordinate(1, 1)
    assert coordinate.getRowAndColumn() == (1, 1)