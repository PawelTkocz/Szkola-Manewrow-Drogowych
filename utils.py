from constants import SCREEN_HEIGHT
from geometry.vector import Point
from schemas import CardinalDirection


def get_pygame_point(point: Point) -> Point:
    return Point(point.x, SCREEN_HEIGHT - point.y)


def clockwise_direction_shift(
    direction: CardinalDirection, steps: int
) -> CardinalDirection:
    directions = [
        CardinalDirection.UP,
        CardinalDirection.RIGHT,
        CardinalDirection.DOWN,
        CardinalDirection.LEFT,
    ]
    index = directions.index(direction)
    new_index = (index + steps) % len(directions)
    return directions[new_index]
