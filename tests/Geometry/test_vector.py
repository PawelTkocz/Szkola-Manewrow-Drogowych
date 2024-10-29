import math
import pytest
from Geometry import Directions, Point, Vector


@pytest.mark.parametrize(
    ["vector", "expected"],
    [
        (Vector(Point(3, 1.14)), Point(3, 1.14)),
        (Vector(Point(3, 1.14), Point(-2.2, 0.1)), Point(5.2, 1.04)),
    ],
)
def test_init(vector: Vector, expected: Point):
    max_rel_tol = 1e-12
    assert math.isclose(vector.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(vector.y, expected.y, rel_tol=max_rel_tol)


@pytest.mark.parametrize(
    ["vector", "expected"],
    [
        (Vector(Point(0, 0)), 0),
        (Vector(Point(-3, 4)), 5),
        (Vector(Point(-3.1, -10.4)), 10.8521887193321),
        (Vector(Point(1.234, 0)), 1.234),
    ],
)
def test_len(vector: Vector, expected: float):
    max_rel_tol = 1e-12
    assert math.isclose(vector.len(), expected, rel_tol=max_rel_tol)


@pytest.mark.parametrize(
    ["vector", "k", "expected"],
    [
        (Vector(Point(0, 0)), 4.1, Vector(Point(0, 0))),
        (Vector(Point(12, 34)), 0, Vector(Point(0, 0))),
        (Vector(Point(-3, 4)), 13.2, Vector(Point(-39.6, 52.8))),
        (Vector(Point(-3.1, -10.4)), -0.2, Vector(Point(0.62, 2.08))),
    ],
)
def test_scale(vector: Vector, k: float, expected: Vector):
    max_rel_tol = 1e-12
    start_len = vector.len()
    scaled_vector = vector.scale(k)
    assert math.isclose(scaled_vector.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(scaled_vector.y, expected.y, rel_tol=max_rel_tol)
    assert math.isclose(scaled_vector.len(), abs(start_len * k), rel_tol=max_rel_tol)
    assert scaled_vector is vector


@pytest.mark.parametrize(
    ["vector", "len", "expected"],
    [
        (Vector(Point(0, 0)), 4.1, Vector(Point(0, 0))),
        (Vector(Point(12, 34)), 0, Vector(Point(0, 0))),
        (Vector(Point(-3, 4)), 10, Vector(Point(-6, 8))),
        (Vector(Point(0, 12.5)), 13.75, Vector(Point(0, 13.75))),
        (
            Vector(Point(-3.1, -10.4)),
            14.15,
            Vector(Point(-4.0420417608347, -13.5603981653809)),
        ),
    ],
)
def test_scale_to_len(vector: Vector, len: float, expected: Vector):
    max_rel_tol = 1e-12
    scaled_vector = vector.scale_to_len(len)
    assert math.isclose(scaled_vector.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(scaled_vector.y, expected.y, rel_tol=max_rel_tol)
    assert scaled_vector is vector


def test_copy():
    vector = Vector(Point(92, 87.33))
    vector_copy = vector.copy()
    assert vector_copy.compare(vector)
    assert vector_copy is not vector
    assert isinstance(vector_copy, Vector)


@pytest.mark.parametrize(
    ["vector", "dir", "len", "expected"],
    [
        (Vector(Point(0, 0)), Directions.LEFT, 4.1, Vector(Point(0, 0))),
        (Vector(Point(10.23, 98.99)), Directions.LEFT, 0, Vector(Point(0, 0))),
        (Vector(Point(10.23, 98.99)), Directions.FRONT, 1, Vector(Point(10.23, 98.99))),
        (Vector(Point(12.56, 0)), Directions.RIGHT, None, Vector(Point(0, -12.56))),
        (Vector(Point(12.56, 0)), Directions.LEFT, None, Vector(Point(0, 12.56))),
        (Vector(Point(12.56, 0)), Directions.LEFT, 15.09, Vector(Point(0, 15.09))),
        (Vector(Point(3, 4)), Directions.RIGHT, 10, Vector(Point(8, -6))),
        (Vector(Point(3, 4)), Directions.LEFT, 10, Vector(Point(-8, 6))),
    ],
)
def test_get_orthogonal_vector(
    vector: Vector, dir: Directions, len: float | None, expected: Vector
):
    max_rel_tol = 1e-12
    start_vector = vector.copy()
    orthogonal_vector = vector.get_orthogonal_vector(dir, len)
    assert math.isclose(orthogonal_vector.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(orthogonal_vector.y, expected.y, rel_tol=max_rel_tol)
    assert orthogonal_vector is not vector
    assert vector.compare(start_vector)


@pytest.mark.parametrize(
    ["vector", "expected"],
    [
        (Vector(Point(2, 0)), Vector(Point(1, 0))),
        (Vector(Point(0, -2)), Vector(Point(0, -1))),
        (Vector(Point(1, 1)), Vector(Point(0.70710678118654, 0.70710678118654))),
        (
            Vector(Point(-14.5, -77.23)),
            Vector(Point(-0.184526721581048, -0.98282749708305)),
        ),
    ],
)
def test_normalize(vector: Vector, expected: Vector):
    max_rel_tol = 1e-12
    normalized_vector = vector.normalize()
    assert math.isclose(normalized_vector.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(normalized_vector.y, expected.y, rel_tol=max_rel_tol)
    assert math.isclose(normalized_vector.len(), 1, rel_tol=max_rel_tol)
    assert normalized_vector is vector


def test_rotate_over_point():
    vector = Vector(Point(2, 3))
    rotated_vector = vector.rotate_over_point(Point(0, 0), math.pi / 2)
    max_rel_tol = 1e-9
    assert math.isclose(rotated_vector.x, -3, rel_tol=max_rel_tol)
    assert math.isclose(rotated_vector.y, 2, rel_tol=max_rel_tol)
    assert rotated_vector is vector
    assert isinstance(rotated_vector, Vector)


def test_add_vector():
    start_vector = Vector(Point(4, 5))
    vector = Vector(Point(-4, -6))
    res = start_vector.add_vector(vector)
    assert res.compare(Vector(Point(0, -1)))
    assert res is start_vector
