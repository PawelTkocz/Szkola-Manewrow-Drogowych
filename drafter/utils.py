import pygame
from geometry import Point, Rectangle, Vector
from utils import get_pygame_point


def apply_y_screen_offset(point: Point, screen_y_offset: int) -> Point:
    return point.add_vector(Vector(Point(0, screen_y_offset)))


def get_pygame_coordinates(
    point: Point, *, scale_factor: float = 1, screen_y_offset: int = 0
) -> tuple[float, float]:
    return get_pygame_point(
        apply_y_screen_offset(Vector(point).scale(scale_factor), screen_y_offset)
    ).to_tuple()


def draw_polygon(
    screen: pygame.Surface,
    color: str,
    corners: list[Point],
    *,
    scale_factor: float = 1,
    screen_y_offset: int = 0,
) -> None:
    pygame_corners = [
        get_pygame_coordinates(
            corner, scale_factor=scale_factor, screen_y_offset=screen_y_offset
        )
        for corner in corners
    ]
    pygame.draw.polygon(screen, color, pygame_corners)


def draw_rectangle(
    screen: pygame.Surface,
    color: str,
    rect: Rectangle,
    *,
    scale_factor: float = 1,
    screen_y_offset: int = 0,
) -> None:
    draw_polygon(
        screen,
        color,
        rect.corners_list,
        scale_factor=scale_factor,
        screen_y_offset=screen_y_offset,
    )


def draw_axis_aligned_rectangle(
    screen: pygame.Surface,
    color: str,
    front_left: Point,
    width: float,
    height: float,
    *,
    scale_factor: float = 1,
    screen_y_offset: int = 0,
    border_front_left_radius: int = -1,
    border_front_right_radius: int = -1,
    border_rear_left_radius: int = -1,
    border_rear_right_radius: int = -1,
    transparency: int = 255,
) -> None:
    transparency = max(0, min(transparency, 255))
    pygame_color = pygame.Color(color)
    pygame_color.a = transparency

    scaled_width = width * scale_factor
    scaled_height = height * scale_factor
    surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
    pygame.draw.rect(
        surface,
        pygame_color,
        pygame.Rect(
            0,
            0,
            scaled_width,
            scaled_height,
        ),
        border_top_right_radius=border_front_right_radius,
        border_top_left_radius=border_front_left_radius,
        border_bottom_left_radius=border_rear_left_radius,
        border_bottom_right_radius=border_rear_right_radius,
    )
    blit_surface(
        screen,
        surface,
        front_left,
        scale_factor=scale_factor,
        screen_y_offset=screen_y_offset,
    )


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
