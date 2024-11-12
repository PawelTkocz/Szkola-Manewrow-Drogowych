import math

import pygame
from Geometry import Directions, Point
import TestBackgroundDrafter
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from cars.BasicBrand import BasicBrand
from cars.Car import Car
import numpy as np
from scipy.spatial import KDTree


class TestCar:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.c1 = Car(
            BasicBrand(),
            Point(
                SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4
            ),
            velocity=0,
        )
        self.background_drafter = TestBackgroundDrafter.TestBackgroundDrafter(
            self.screen_width, self.screen_height
        )

    def turn_left(self):
        self.c1.turn(Directions.LEFT)

    def turn_right(self):
        self.c1.turn(Directions.RIGHT)

    def draw(self):
        self.background_drafter.draw(self.screen)
        self.c1.draw(self.screen)

        self.turn_points = [
            (SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
            (SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2),
            (SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2),
        ]
        p0, p1, p2, p3 = self.turn_points
        t_values = np.linspace(0, 1, 100)
        curve_points = [cubic_bezier(t, p0, p1, p2, p3) for t in t_values]
        tree = KDTree(curve_points)
        for point in self.turn_points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 5)
        for i in range(len(curve_points) - 1):
            pygame.draw.line(
                self.screen, (0, 255, 0), curve_points[i], curve_points[i + 1], 2
            )

        distance, index = tree.query([self.c1.front_middle.x, self.c1.front_middle.y])
        closest_point = curve_points[index]
        pygame.draw.circle(self.screen, (0, 0, 255), closest_point, 5)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def next_frame(self):
        self.c1.move()

    def speed_up_front(self):
        self.c1.speed_up(Directions.FRONT)

    def speed_up_reverse(self):
        self.c1.speed_up(Directions.BACK)

    def brake(self):
        self.c1.brake()


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
