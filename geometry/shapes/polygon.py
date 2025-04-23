from pygame import Surface
import pygame
from drafter.utils import get_pygame_coordinates
from geometry.shapes.shape import Shape
from geometry.vector import Point


class Polygon(Shape):
    def __init__(self, corners: list[Point], color: str) -> None:
        self._corners = corners
        self.color = color

    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        pygame_corners = [
            get_pygame_coordinates(
                corner, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            )
            for corner in self._corners
        ]
        pygame.draw.polygon(screen, self.color, pygame_corners)
