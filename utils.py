from constants import SCREEN_HEIGHT
from geometry import Point


def get_pygame_point(point: Point) -> Point:
    return Point(point.x, SCREEN_HEIGHT - point.y)
