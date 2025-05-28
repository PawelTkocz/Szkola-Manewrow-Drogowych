import os
import sys
from pygame import Surface
import pygame
from constants import FONTS_DIR_PATH, IMAGES_DIR_PATH
from geometry.vector import Point
from schemas import CardinalDirection


def flip_y_axis(screen: Surface, point: Point) -> Point:
    return Point(point.x, screen.get_height() - point.y)


def blit_surface(
    screen: Surface,
    surface: Surface,
    top_left: Point,
) -> None:
    screen.blit(
        surface,
        flip_y_axis(screen, top_left).to_tuple(),
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


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


def load_image(file_name: str) -> Surface:
    return pygame.image.load(resource_path(os.path.join(IMAGES_DIR_PATH, file_name)))


def load_font(font_file_name: str, size: int) -> pygame.font.Font:
    return pygame.font.Font(
        resource_path(os.path.join(FONTS_DIR_PATH, font_file_name)), size
    )
