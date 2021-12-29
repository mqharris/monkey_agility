from mouse.Path import Path
import numpy as np
import pytest


def test_path():
    data = [[i, i] for i in range(6)]
    path = Path(data)
    path.get_relative_path()
    path.get_abs_path()
    assert path.length == pytest.approx(7.07107)
    assert path.num_points == 6
    assert path.rel_path == [[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
    assert path.data == path.abs_path


def test_create_new_path():
    data = [[i, i] for i in range(6)]
    times = [i for i in range(6)]
    path = Path(data, times)
    new_path, new_times = path.create_path_to([12, 6])
    path2 = Path(new_path, np.cumsum(new_times))
    expected_scale_factor = 1.8973665961010275
    assert abs(expected_scale_factor * path.length - path2.length) < 1e-2
    assert abs((expected_scale_factor *
               sum(path.times)) - sum(path2.times)) < 1e-2


if __name__ == "__main__":
    test_path()
    test_create_new_path()
