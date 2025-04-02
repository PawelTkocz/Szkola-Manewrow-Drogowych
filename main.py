import pygame

from animations.animations_menus.main_menu import MainMenu
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from state import State

pygame.init()
clock = pygame.time.Clock()


class DrivingManoeuvresApplication:
    def __init__(self, start_state: State, screen: pygame.Surface) -> None:
        self.screen = screen
        self.current_state = start_state

    def render_frame(self) -> None:
        self.current_state.render_frame(self.screen)

    def handle_click(self, mouse_click_position: tuple[float, float]) -> None:
        self.current_state = self.current_state.handle_click(mouse_click_position)

    def handle_quit(self) -> None:
        self.current_state.handle_quit()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
driving_manoeuvres_application = DrivingManoeuvresApplication(MainMenu(), screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            driving_manoeuvres_application.handle_quit()
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            driving_manoeuvres_application.handle_click(pygame.mouse.get_pos())
    driving_manoeuvres_application.render_frame()
    pygame.display.update()
    clock.tick(30)
