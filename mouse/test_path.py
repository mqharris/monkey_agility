import pytest
from path_analysis import Path


def test_path():
    data = [[i, i] for i in range(6)]

    path = Path(data)

    assert path.length == pytest.approx(7.07107)
    assert path.num_points == 6

    path.get_relative_path()

    assert path.rel_path == [[0, 0], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]

    path.get_abs_path()

    assert path.data == path.abs_path


def test_create_new_path():
    data = [[i, i] for i in range(6)]
    path = Path(data)
    print(path.rel_path)

    new_path = path.create_path_to([12, 6])


if __name__ == "__main__":
    test_path()
    test_create_new_path()
