import math

import pygame
from Geometry import Directions, Point
import TestBackgroundDrafter
from autonomousDriving.BasicAutonomousDriving import BasicAutonomousDriving
from cars.BasicBrand import BasicBrand
from cars.Car import Car
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree


class TestAutonomusTurn:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.turn_points = [(400, 400), (800, 500), (1200, 400)]
        x_points, y_points = zip(*self.turn_points)  # Separate x and y coordinates

        # Create a cubic spline that passes through the specified points
        spline_x = np.linspace(
            min(x_points), max(x_points), 500
        )  # X values for smooth curve
        spline = CubicSpline(x_points, y_points)  # Create the spline
        spline_y = spline(spline_x)  # Evaluate Y values along the spline

        # Convert spline points to integer coordinates for Pygame
        self.curve_points = [(int(x), int(y)) for x, y in zip(spline_x, spline_y)]
        self.tree = KDTree(self.curve_points)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.car = Car(BasicBrand(), Point(400, 400), velocity=0)
        self.background_drafter = TestBackgroundDrafter.TestBackgroundDrafter(
            self.screen_width, self.screen_height
        )

        self.autonomous_driving = BasicAutonomousDriving(self.car, self.curve_points)

    def draw(self):
        self.background_drafter.draw(self.screen)
        self.car.draw(self.screen)

        for point in self.turn_points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 5)
        for i in range(len(self.curve_points) - 1):
            pygame.draw.line(
                self.screen,
                (0, 255, 0),
                self.curve_points[i],
                self.curve_points[i + 1],
                2,
            )

        distance, index = self.tree.query(
            [self.car.front_left.x, self.car.front_left.y]
        )
        closest_point = self.curve_points[index]
        pygame.draw.circle(self.screen, (0, 0, 255), closest_point, 5)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def next_frame(self):
        self.autonomous_driving.simulate_move()


pygame.init()
clock = pygame.time.Clock()
game = TestAutonomusTurn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.draw()
    game.next_frame()
    pygame.display.update()
    clock.tick(50)
