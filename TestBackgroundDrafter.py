import pygame


class TestBackgroundDrafter:
    """
    Class responsible for drawing test background
    """

    street_color = "#383838"

    def __init__(self, screen_width, screen_height):
        self.screen_height = screen_height
        self.screen_width = screen_width

    def draw(self, screen):
        self.screen = screen
        self.screen.fill(self.street_color)
