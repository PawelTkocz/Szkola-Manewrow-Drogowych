from geometry.vector import Point


class Circle:
    def __init__(self, center: Point, radius: float) -> None:
        self.center = center.copy()
        self.radius = radius


# maybe create class Angle for wheels angle and class Direction whill extend this class
