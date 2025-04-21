import math
import pytest

from geometry.vector import Point, Vector


def test_init() -> None:
    point = Point(3, 1.14)
    assert point.x == 3
    assert point.y == 1.14


@pytest.mark.parametrize(
    ["point", "expected"],
    [
        (Point(10, 19), False),
        (Point(1, 3.5), False),
        (Point(-1, 2.5), False),
        (Point(1, 2.5), True),
    ],
)
def test_compare(point: Point, expected: bool) -> None:
    assert Point(1, 2.5).compare(point) == expected


@pytest.mark.parametrize(
    ["point", "vector", "expected"],
    [
        (Point(34, 43), Vector(Point(0, 0)), Point(34, 43)),
        (Point(0, 0), Vector(Point(-1.2, -3.4)), Point(-1.2, -3.4)),
        (Point(3, 4), Vector(Point(-5, 8.9)), Point(-2, 12.9)),
        (Point(-7.7, 10), Vector(Point(-2.2, -11)), Point(-9.9, -1)),
        (Point(-100, -99), Vector(Point(100, 99)), Point(0, 0)),
    ],
)
def test_add_vector(point: Point, vector: Vector, expected: Point) -> None:
    res = point.add_vector(vector)
    assert res.compare(expected)
    assert res is point


def test_add_vector_composed() -> None:
    point = Point(3, 4)
    res = point.add_vector(Vector(Point(6, 8))).add_vector(Vector(Point(10, 10)))
    assert point.compare(Point(19, 22))
    assert res is point


def test_copy() -> None:
    point = Point(92, 87.33)
    point_copy = point.copy()
    assert point_copy.compare(point)
    assert point_copy is not point


@pytest.mark.parametrize(
    ["point", "rotate_point", "angle", "expected"],
    [
        (Point(3, 5), Point(0, 0), math.pi / 2, Point(-5, 3)),
        (Point(3, 5), Point(0, 0), math.pi / -2, Point(5, -3)),
        (Point(3, 5), Point(0, 0), 0, Point(3, 5)),
        (
            Point(3.14, 15.92),
            Point(-5.55, -9.91),
            math.pi / 3,
            Point(-23.5744361797520, 10.5307607588867),
        ),
        (
            Point(3.14, 15.92),
            Point(-5.55, -9.91),
            math.pi / -3,
            Point(21.1644361797520, -4.5207607588867),
        ),
    ],
)
def test_rotate_over_point(
    point: Point, rotate_point: Point, angle: float, expected: Point
) -> None:
    rotated_point = point.rotate_over_point(rotate_point, angle)
    max_rel_tol = 1e-9
    assert math.isclose(rotated_point.x, expected.x, rel_tol=max_rel_tol)
    assert math.isclose(rotated_point.y, expected.y, rel_tol=max_rel_tol)
    assert rotated_point is point


def test_rotate_over_point_compose() -> None:
    start_point = Point(1234.56, -3.8)
    point = start_point.copy()
    rotate_point = Point(23.1, 43.3)
    n = 1000
    for i in range(n):
        point.rotate_over_point(rotate_point, 2 * math.pi / n)
    max_rel_tol = 1e-12
    assert math.isclose(point.x, start_point.x, rel_tol=max_rel_tol)
    assert math.isclose(point.y, start_point.y, rel_tol=max_rel_tol)
