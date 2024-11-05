import math

import pygame
from Geometry import Point, Vector
import TestBackgroundDrafter
from cars.BasicBrand import BasicBrand
from cars.Car import Car


class TestCar:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.c1 = Car(BasicBrand(), Point(400, 400), velocity=0)
        self.background_drafter = TestBackgroundDrafter.TestBackgroundDrafter(
            self.screen_width, self.screen_height
        )

    def draw(self):
        self.background_drafter.draw(self.screen)
        self.c1.draw(self.screen)

    def next_frame(self):
        self.c1.move()


pygame.init()
clock = pygame.time.Clock()
game = TestCar()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        game.turn_left()
    elif keys[pygame.K_RIGHT]:
        game.turn_right()
    if keys[pygame.K_UP]:
        game.speed_up_front()
    elif keys[pygame.K_SPACE]:
        game.brake()
    elif keys[pygame.K_DOWN]:
        game.speed_up_reverse()

    game.draw()
    game.next_frame()
    pygame.display.update()
    clock.tick(60)
