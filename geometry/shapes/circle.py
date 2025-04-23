from pygame import Surface
import pygame
from drafter.utils import get_pygame_coordinates
from geometry.shapes.shape import Shape
from geometry.vector import Point


class Circle(Shape):
    def __init__(self, center: Point, radius: float, color: str) -> None:
        self.center = center.copy()
        self.radius = radius
        self.color = color

    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        pygame.draw.circle(
            screen,
            self.color,
            get_pygame_coordinates(
                self.center, scale_factor=scale_factor, screen_y_offset=screen_y_offset
            ),
            self.radius * scale_factor,
        )
