from pygame import Surface
import pygame
from application_screen import ApplicationScreen
from constants import IMAGES_DIR_PATH, SCREEN_HEIGHT
from geometry.shapes.circle import Circle
from geometry.vector import Point
from utils import blit_surface


class PreviousScreenButton:
    def __init__(
        self,
        previous_app_screen: ApplicationScreen,
        circle: Circle = Circle(Point(50, SCREEN_HEIGHT - 50), 50),
    ) -> None:
        self.image = pygame.transform.scale(
            pygame.image.load(f"{IMAGES_DIR_PATH}/previous_screen_button.png"),
            (circle.diameter, circle.diameter),
        )
        self.previous_app_screen = previous_app_screen
        self.circle = circle
        self.image_top_left = Point(
            circle.center.x - circle.radius, circle.center.y + circle.radius
        )

    def render(self, screen: Surface) -> None:
        blit_surface(screen, self.image, self.image_top_left)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen | None:
        if self.circle.is_point_inside(mouse_click_point):
            return self.previous_app_screen
        return None
