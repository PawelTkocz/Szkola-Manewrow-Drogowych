from pygame import Surface
import pygame
from geometry.shapes.shape import Shape
from geometry.vector import Point
from utils import get_pygame_screen_point


class Polygon(Shape):
    def __init__(self, corners: list[Point], color: str) -> None:
        self._corners = corners
        self.color = color

    def draw(self, screen: Surface) -> None:
        pygame_corners = [
            get_pygame_screen_point(corner).to_tuple() for corner in self._corners
        ]
        pygame.draw.polygon(screen, self.color, pygame_corners)
