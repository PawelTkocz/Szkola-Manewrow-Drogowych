from typing import List
from pygame import Surface
import pygame
from Geometry import Point, Rectangle

# OK


def tuples_list(point_list: List[Point]):
    """
    Convert list of points to list of tuples
    """
    return [(p.x, p.y) for p in point_list]


class BasicBrandDrafter:
    """
    Class responsible for drawing basic brand car on the screen
    """

    def __init__(self, width: float, length: float, color: str):
        """
        Initialize the drafter of basic brand cars

        :param width: width of the car
        :param length: length of the car
        :param color: color of the car
        """
        self.width = width
        self.length = length
        self.color = color

    def draw(self, body: Rectangle, screen: Surface) -> None:
        """
        Draw the car on the screen

        :param body: Rectangle representing position of the car body
        :param screen: pygame screen to draw the car on
        """
        pygame.draw.polygon(screen, "black", tuples_list(body.corners_list))
