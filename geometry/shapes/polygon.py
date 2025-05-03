from pygame import Surface
import pygame
from geometry.shapes.shape import Shape
from geometry.vector import Point
from utils import flip_y_axis


class Polygon(Shape):
    def __init__(self, corners: list[Point], color: str) -> None:
        self.corners = corners
        self.color = color

    def draw(self, screen: Surface) -> None:
        pygame_corners = [
            flip_y_axis(screen, corner).to_tuple() for corner in self.corners
        ]
        pygame.draw.polygon(screen, self.color, pygame_corners)
