import pygame

from Constants import SCREEN_HEIGHT, SCREEN_WIDTH
from MainMenu import MainMenu
from State import State

pygame.init()
clock = pygame.time.Clock()


class DrivingManoeuvresApplication:
    def __init__(self, start_state: State):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_state = start_state

    def render_frame(self):
        self.current_state.render_frame(self.screen)

    def handle_click(self, mouse_click_position):
        self.current_state = self.current_state.handle_click(mouse_click_position)


driving_manoeuvres_application = DrivingManoeuvresApplication(MainMenu())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            driving_manoeuvres_application.handle_click(pygame.mouse.get_pos())
    driving_manoeuvres_application.render_frame()
    pygame.display.update()
    clock.tick(30)
