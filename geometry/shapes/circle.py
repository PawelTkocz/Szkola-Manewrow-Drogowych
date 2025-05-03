from geometry.shapes.shape import Shape
from geometry.vector import Point


class Circle(Shape):
    def __init__(self, center: Point, radius: float, color: str) -> None:
        self.center = center.copy()
        self.radius = radius
        self.color = color
