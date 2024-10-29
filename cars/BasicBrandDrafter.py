import pygame


def tuples_list(point_list):
    return [(p.x, p.y) for p in point_list]


class BasicBrandDrafter:
    """
    Class responsible for drawing basic brand car on the screen
    """

    def __init__(self, width, length, color):
        self.width = width
        self.length = length
        self.color = color

    def draw(self, corners, screen):
        self.rear_left, self.rear_right, self.front_right, self.front_left = corners
        self.screen = screen
        pygame.draw.polygon(screen, "black", tuples_list(corners))
