import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from animations.constants import LINES_COLOR, PAVEMENT_COLOR, STREET_COLOR
from animations.intersection.constants import (
    LINES_WIDTH,
    ROAD_WIDTH,
)


class IntersectionDrafter:
    """
    Class responsible for drawing the intersection.
    """

    def draw_street(self, screen):
        pygame.draw.rect(
            screen,
            STREET_COLOR,
            pygame.Rect(
                (SCREEN_WIDTH - ROAD_WIDTH) / 2,
                0,
                ROAD_WIDTH,
                SCREEN_HEIGHT,
            ),
        )
        pygame.draw.rect(
            screen,
            STREET_COLOR,
            pygame.Rect(
                0,
                (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                SCREEN_WIDTH,
                ROAD_WIDTH,
            ),
        )

    def draw_lines(self, screen):
        pygame.draw.rect(
            screen,
            LINES_COLOR,
            pygame.Rect(
                (SCREEN_WIDTH) / 2,
                0,
                LINES_WIDTH,
                (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
            ),
        )
        pygame.draw.rect(
            screen,
            LINES_COLOR,
            pygame.Rect(
                0,
                SCREEN_HEIGHT / 2,
                (SCREEN_WIDTH - ROAD_WIDTH) / 2,
                LINES_WIDTH,
            ),
        )
        pygame.draw.rect(
            screen,
            LINES_COLOR,
            pygame.Rect(
                (SCREEN_WIDTH) / 2,
                SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                LINES_WIDTH,
                (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
            ),
        )
        pygame.draw.rect(
            screen,
            LINES_COLOR,
            pygame.Rect(
                SCREEN_WIDTH - (SCREEN_WIDTH - ROAD_WIDTH) / 2,
                SCREEN_HEIGHT / 2,
                (SCREEN_WIDTH - ROAD_WIDTH) / 2,
                LINES_WIDTH,
            ),
        )

    def draw(self, screen):
        screen.fill(PAVEMENT_COLOR)
        self.draw_street(screen)
        self.draw_lines(screen)
