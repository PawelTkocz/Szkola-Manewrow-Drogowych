from pygame import Surface
from geometry.vector import Point
from schemas import CardinalDirection


def get_pygame_screen_point(screen: Surface, point: Point) -> Point:
    return Point(point.x, screen.get_height() - point.y)


def blit_surface(
    screen: Surface,
    surface: Surface,
    top_left: Point,
) -> None:
    screen.blit(
        surface,
        get_pygame_screen_point(screen, top_left).to_tuple(),
    )


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
