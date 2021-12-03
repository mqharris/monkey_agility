from utils import get_angle, rotate
from path_analysis import Path, get_absolute_path
import math


def test_get_angle():
    assert get_angle([[0, 0], [1, 1]]) == math.radians(45)
    assert get_angle([[0, 0], [1, 0]]) == math.radians(0)
    assert get_angle([[0, 0], [0, 1]]) == math.radians(90)
    assert get_angle([[0, 0], [-1, -1]]) == math.radians(225)
    assert get_angle([[0, 0], [-1, 1]]) == math.radians(135)
    assert get_angle([[0, 0], [1, -1]]) == math.radians(315)
    assert get_angle([[0, 0], [0, -1]]) == math.radians(270)


def test_rotate():

    data = [[0, 0], [0, 1], [1, 1]]
    path = Path(data)
    path.get_relative_path()

    rotated_path = rotate(path.rel_path, 90)
    assert rotated_path == [[0, 0], [-1.0, 0.0], [0.0, 1.0]]

    abs_path = get_absolute_path(rotated_path)

    r_path = Path(abs_path)

    assert path.length == r_path.length


if __name__ == "__main__":
    test_get_angle()
    test_rotate()
