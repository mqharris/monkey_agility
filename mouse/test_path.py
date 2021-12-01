import pytest
from path_analysis import Path


def testPath():
    data = [[i, i] for i in range(6)]

    path = Path(data)

    assert path.length == pytest.approx(7.07107)
    assert path.num_points == 6
