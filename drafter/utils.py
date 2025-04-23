import pygame
from geometry.vector import Point, Vector
from utils import get_pygame_point


def apply_y_screen_offset(point: Point, screen_y_offset: int) -> Point:
    return point.add_vector(Vector(Point(0, screen_y_offset)))


def get_pygame_coordinates(
    point: Point, *, scale_factor: float = 1, screen_y_offset: int = 0
) -> tuple[float, float]:
    return get_pygame_point(
        apply_y_screen_offset(Vector(point).scale(scale_factor), screen_y_offset)
    ).to_tuple()


def blit_surface(
    screen: pygame.Surface,
    surface: pygame.Surface,
    top_left: Point,
    *,
    scale_factor: float = 1,
    screen_y_offset: int = 0,
) -> None:
    screen.blit(
        surface,
        get_pygame_coordinates(
            top_left, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        ),
    )
