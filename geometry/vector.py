from __future__ import annotations
import math

from schemas import HorizontalDirection


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def compare(self, point: Point) -> bool:
        return self.x == point.x and self.y == point.y

    def add_vector(self, vec: Vector) -> Point:
        self.x += vec.x
        self.y += vec.y
        return self

    def distance(self, point: Point) -> float:
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def copy(self) -> Point:
        return Point(self.x, self.y)

    def rotate_over_point(self, rotate_point: Point, angle: float) -> Point:
        sin = math.sin(angle)
        cos = math.cos(angle)

        v = Vector(end=self, start=rotate_point)
        v_rotated = Vector(
            Point(v.x * cos - v.y * sin, v.x * sin + v.y * cos)
        ).scale_to_len(v.length())
        rotated_point = rotate_point.copy().add_vector(v_rotated)
        self.x = rotated_point.x
        self.y = rotated_point.y
        return self

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


class Vector(Point):
    def __init__(self, end: Point, start: Point = Point(0, 0)) -> None:
        super().__init__(end.x - start.x, end.y - start.y)

    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def scale(self, k: float) -> Vector:
        self.x *= k
        self.y *= k
        return self

    def scale_to_len(self, len: float) -> Vector:
        if self.length() == 0:
            return self
        else:
            return self.scale(len / self.length())

    def get_orthogonal_vector(
        self, dir: HorizontalDirection, len: float | None = None
    ) -> Vector:
        v = (
            Vector(Point(self.y, -1 * self.x))
            if dir == HorizontalDirection.RIGHT
            else Vector(Point(-1 * self.y, self.x))
        )
        return v.scale_to_len(len) if len is not None else v

    def get_negative_of_a_vector(self) -> Vector:
        return self.copy().scale(-1)

    def normalize(self) -> Vector:
        return self.scale_to_len(1)

    def add_vector(self, vector: Vector) -> Vector:
        self.x += vector.x
        self.y += vector.y
        return self

    def copy(self) -> Vector:
        return Vector(self)
