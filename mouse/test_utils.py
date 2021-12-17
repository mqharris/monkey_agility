from mouse.utils import get_angle, rotate, scale
from mouse.pathClass import Path, get_absolute_path
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

    rotated_path = rotate(path.rel_path, math.radians(90))
    assert rotated_path == [[0, 0], [-1.0, 0.0], [0.0, 1.0]]

    dummy_time_data = [0 for _ in range(len(rotated_path))]
    abs_path = get_absolute_path(rotated_path)

    r_path = Path(abs_path)

    assert path.length == r_path.length


def test_scale():

    data = [[i, i] for i in range(0, 10, 2)]

    path = Path(data)
    path.get_relative_path()

    scaled_path = scale(path.rel_path, 0.8)

    assert scaled_path == [[0, 0], [1.6, 1.6],
                           [1.6, 1.6], [1.6, 1.6], [1.6, 1.6]]

    abs_path = get_absolute_path(scaled_path)

    assert abs_path == [[0, 0], [1.6, 1.6], [3.2, 3.2], [
        4.800000000000001, 4.800000000000001], [6.4, 6.4]]


if __name__ == "__main__":
    test_get_angle()
    test_rotate()
    test_scale()
