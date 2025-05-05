from geometry.vector import Point


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center.copy()
        self.radius = radius

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    def is_point_inside(self, point: Point) -> bool:
        return self.center.distance(point) <= self.radius
