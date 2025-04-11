from pygame import Surface
import pygame
from application_screen.application_screen import ApplicationScreen
from geometry import Direction, Point, Rectangle


class BackNavigableApplicationScreen(ApplicationScreen):
    def __init__(
        self, app_screen: ApplicationScreen, previous_app_screen: ApplicationScreen
    ) -> None:
        self.app_screen = app_screen
        self.previous_app_screen = previous_app_screen
        self.button_rectangle = Rectangle(
            Point(50, 0), 100, 100, Direction(Point(0, 1))
        )

    def render_button(self, screen: Surface) -> None:
        rect_surface = pygame.Surface(
            (self.button_rectangle.width, self.button_rectangle.length), pygame.SRCALPHA
        )
        rect_surface.fill((0, 0, 255, 128))
        screen.blit(rect_surface, (0, 0))

    def render_frame(self, screen: Surface) -> None:
        self.app_screen.render_frame(screen)
        self.render_button(screen)

    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> ApplicationScreen:
        if self.button_rectangle.is_point_inside(Point(*mouse_click_position)):
            return self.previous_app_screen
        return self.app_screen.handle_click(mouse_click_position)
