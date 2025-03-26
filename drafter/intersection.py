import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from road_segments.constants import LINES_WIDTH
from road_segments.intersection.schemas import IntersectionColors, IntersectionParts


class IntersectionDrafter:
    """
    Class responsible for drawing the intersection.
    """

    def __init__(
        self,
        intersection_parts: IntersectionParts,
        intersection_colors: IntersectionColors,
    ):
        self.intersection_parts = intersection_parts
        self.intersection_colors = intersection_colors
        self.road_width = self.intersection_parts["intersection_area"].width // 2

    def draw_street(self, screen):
        pygame.draw.rect(
            screen,
            self.intersection_colors["street_color"],
            pygame.Rect(
                (SCREEN_WIDTH - self.road_width) / 2,
                0,
                self.road_width,
                SCREEN_HEIGHT,
            ),
        )
        pygame.draw.rect(
            screen,
            self.intersection_colors["street_color"],
            pygame.Rect(
                0,
                (SCREEN_HEIGHT - self.road_width) / 2,
                SCREEN_WIDTH,
                self.road_width,
            ),
        )

    def draw_lines(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.intersection_colors["lines_color"],
            pygame.Rect(
                (SCREEN_WIDTH) / 2,
                0,
                LINES_WIDTH,
                (SCREEN_HEIGHT - self.road_width) / 2,
            ),
        )
        pygame.draw.rect(
            screen,
            self.intersection_colors["lines_color"],
            pygame.Rect(
                0,
                SCREEN_HEIGHT / 2,
                (SCREEN_WIDTH - self.road_width) / 2,
                LINES_WIDTH,
            ),
        )
        pygame.draw.rect(
            screen,
            self.intersection_colors["lines_color"],
            pygame.Rect(
                (SCREEN_WIDTH) / 2,
                SCREEN_HEIGHT - (SCREEN_HEIGHT - self.road_width) / 2,
                LINES_WIDTH,
                (SCREEN_HEIGHT - self.road_width) / 2,
            ),
        )
        pygame.draw.rect(
            screen,
            self.intersection_colors["lines_color"],
            pygame.Rect(
                SCREEN_WIDTH - (SCREEN_WIDTH - self.road_width) / 2,
                SCREEN_HEIGHT / 2,
                (SCREEN_WIDTH - self.road_width) / 2,
                LINES_WIDTH,
            ),
        )

    def draw(self, screen: pygame.Surface):
        screen.fill(self.intersection_colors["pavement_color"])
        self.draw_street(screen)
        self.draw_lines(screen)
