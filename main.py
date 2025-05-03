import pygame

from animations.animations_menus.interesction_manoeuvres_menus.main_menu import MainMenu
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry.vector import Point
from screen_manager import get_screen, init_screen
from utils import get_pygame_screen_point

pygame.init()
clock = pygame.time.Clock()


class IntersectionManoeuvresApplication:
    def __init__(
        self, start_app_screen: ApplicationScreen, screen: pygame.Surface
    ) -> None:
        self.screen = screen
        self.current_app_screen = start_app_screen

    def render_frame(self) -> None:
        self.current_app_screen.render_frame(self.screen)

    def handle_click(self, mouse_click_position: tuple[float, float]) -> None:
        self.current_app_screen = self.current_app_screen.handle_click(
            get_pygame_screen_point(self.screen, Point(*mouse_click_position))
        )


init_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = get_screen()
intersection_manoeuvres_application = IntersectionManoeuvresApplication(
    MainMenu(screen),
    screen,
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            intersection_manoeuvres_application.handle_click(pygame.mouse.get_pos())
    intersection_manoeuvres_application.render_frame()
    pygame.display.update()
    clock.tick(30)
