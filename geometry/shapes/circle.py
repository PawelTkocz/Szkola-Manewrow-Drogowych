from geometry.vector import Point


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center.copy()
        self.radius = radius

    def is_point_inside(self, point: Point) -> bool:
        return self.center.distance(point) <= self.radius
