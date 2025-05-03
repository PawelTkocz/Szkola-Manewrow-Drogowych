from pygame import Surface
from geometry.vector import Point
from schemas import CardinalDirection
from screen_manager import get_screen


def get_pygame_screen_point(point: Point) -> Point:
    return Point(point.x, get_screen().get_height() - point.y)


def blit_surface(
    surface: Surface,
    top_left: Point,
) -> None:
    get_screen().blit(
        surface,
        get_pygame_screen_point(top_left).to_tuple(),
    )


def clockwise_direction_shift(
    direction: CardinalDirection, shifts_number: int
) -> CardinalDirection:
    directions = [
        CardinalDirection.UP,
        CardinalDirection.RIGHT,
        CardinalDirection.DOWN,
        CardinalDirection.LEFT,
    ]
    index = directions.index(direction)
    new_index = (index + shifts_number) % len(directions)
    return directions[new_index]
