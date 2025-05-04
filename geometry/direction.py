from __future__ import annotations
from geometry.vector import Point, Vector


class Direction(Vector):
    def __init__(self, end: Point, start: Point = Point(0, 0)) -> None:
        super().__init__(end, start)
        super().normalize()

    def turn(self, angle: float) -> Direction:
        super().rotate_over_point(Point(0, 0), angle)
        super().normalize()
        return self

    def copy(self) -> Direction:
        return Direction(self)
