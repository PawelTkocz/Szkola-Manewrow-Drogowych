from pygame import Surface
import pygame
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT
from drafter.drafter_base import DrafterBase
from geometry import Direction, Point, Rectangle


class PreviousScreenButton:
    def __init__(
        self,
        previous_app_screen: ApplicationScreen,
        rectangle: Rectangle = Rectangle(
            Point(50, SCREEN_HEIGHT), 100, 100, Direction(Point(0, 1))
        ),
    ) -> None:
        self.image = pygame.transform.scale(
            pygame.image.load(
                "animations/animations_menus/screenshots/go_back_button.png"
            ),
            (rectangle.width, rectangle.length),
        )
        self.previous_app_screen = previous_app_screen
        self.rectangle = rectangle

    def render(self, screen: Surface) -> None:
        DrafterBase().blit_surface(screen, self.image, self.rectangle.front_left)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        if self.rectangle.is_point_inside(mouse_click_point):
            return self.previous_app_screen
        return None
