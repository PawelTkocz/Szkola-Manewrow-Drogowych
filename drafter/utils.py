import pygame

from constants import SCREEN_HEIGHT
from geometry import Point, Rectangle


def _get_pygame_coordinates(point: Point) -> tuple[float, float]:
    return [point.x, SCREEN_HEIGHT - point.y]


def draw_polygon(screen: pygame.Surface, color: str, corners: list[Point]) -> None:
    pygame_corners = [_get_pygame_coordinates(corner) for corner in corners]
    pygame.draw.polygon(screen, color, pygame_corners)


def draw_rectangle(screen: pygame.Surface, color: str, rect: Rectangle) -> None:
    draw_polygon(screen, color, rect.corners_list)


def draw_circle(
    screen: pygame.Surface, color: str, center: Point, radius: float
) -> None:
    pygame.draw.circle(screen, color, _get_pygame_coordinates(center), radius)
