import math

import pygame
from Geometry import Directions, Point
import TestBackgroundDrafter
from cars.BasicBrand import BasicBrand
from cars.Car import Car
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree


class TestCar:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.c1 = Car(BasicBrand(), Point(400, 400), velocity=0)
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
        points = [(100, 300), (200, 100), (400, 500), (600, 150), (700, 400)]
        x_points, y_points = zip(*points)  # Separate x and y coordinates

        # Create a cubic spline that passes through the specified points
        spline_x = np.linspace(
            min(x_points), max(x_points), 500
        )  # X values for smooth curve
        spline = CubicSpline(x_points, y_points)  # Create the spline
        spline_y = spline(spline_x)  # Evaluate Y values along the spline

        # Convert spline points to integer coordinates for Pygame
        curve_points = [(int(x), int(y)) for x, y in zip(spline_x, spline_y)]
        tree = KDTree(curve_points)
        for point in points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 5)
        for i in range(len(curve_points) - 1):
            pygame.draw.line(
                self.screen, (0, 255, 0), curve_points[i], curve_points[i + 1], 2
            )

        distance, index = tree.query([self.c1.front_left.x, self.c1.front_left.y])
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
