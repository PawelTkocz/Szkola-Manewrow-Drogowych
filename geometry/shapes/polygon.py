from pygame import Surface
import pygame
from geometry.vector import Point
from utils import flip_y_axis


class Polygon:
    def __init__(self, corners: list[Point], color: str) -> None:
        if len(corners) < 3:
            raise ValueError("Polygon must have at least 3 corners.")
        self.corners = corners
        self.color = color

    def draw(self, screen: Surface) -> None:
        pygame_corners = [
            flip_y_axis(screen, corner).to_tuple() for corner in self.corners
        ]
        pygame.draw.polygon(screen, self.color, pygame_corners)
