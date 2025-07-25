import sys
import pygame

from animations.animations_menus.interesction_manoeuvres_menus.main_menu import MainMenu
from application_screen import ApplicationScreen
from constants import CLOCK_TICK, SCREEN_HEIGHT, SCREEN_WIDTH
from geometry.vector import Point
from screen_manager import get_screen, init_screen
from utils import flip_y_axis

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
init_screen(SCREEN_WIDTH, SCREEN_HEIGHT)


class IntersectionManoeuvresApplication:
    def __init__(self) -> None:
        self.screen = get_screen()
        self.current_app_screen: ApplicationScreen = MainMenu()

    def render_frame(self) -> None:
        self.current_app_screen.render_frame(self.screen)

    def handle_click(self, mouse_click_position: tuple[float, float]) -> None:
        self.current_app_screen = self.current_app_screen.handle_click(
            flip_y_axis(self.screen, Point(*mouse_click_position))
        )


intersection_manoeuvres_application = IntersectionManoeuvresApplication()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            intersection_manoeuvres_application.handle_click(pygame.mouse.get_pos())
    intersection_manoeuvres_application.render_frame()
    pygame.display.update()
    clock.tick(CLOCK_TICK)
