import math

from Geometry import Directions, Point
from animations.intersection.IntersectionDrafter import IntersectionDrafter
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import BasicAutonomousDriving
from cars.BasicBrand import BasicBrand
from cars.Car import Car

import pygame
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree


def cubic_bezier(t, p0, p1, p2, p3):
    x = (
        (1 - t) ** 3 * p0[0]
        + 3 * (1 - t) ** 2 * t * p1[0]
        + 3 * (1 - t) * t**2 * p2[0]
        + t**3 * p3[0]
    )
    y = (
        (1 - t) ** 3 * p0[1]
        + 3 * (1 - t) ** 2 * t * p1[1]
        + 3 * (1 - t) * t**2 * p2[1]
        + t**3 * p3[1]
    )
    return x, y


def get_points():
    margin = 0
    track_points = [
        (x, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4)
        for x in np.linspace(0, SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, 500)
    ]
    turn_points = [
        (SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
        (2 * margin + SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
        (
            1 * margin + SCREEN_WIDTH / 2 + ROAD_WIDTH / 4,
            SCREEN_HEIGHT / 2 + 0 * margin,
        ),
        (
            1 * margin + SCREEN_WIDTH / 2 + ROAD_WIDTH / 4,
            SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2,
        ),
    ]
    p0, p1, p2, p3 = turn_points
    t_values = np.linspace(0, 1, 200)
    curve_points = [cubic_bezier(t, p0, p1, p2, p3) for t in t_values]
    track_points.extend(curve_points)
    t_values = np.linspace(0, margin, 200)
    for i in range(-1000, SCREEN_HEIGHT // 2 - ROAD_WIDTH // 2):
        track_points.append((SCREEN_WIDTH / 2 + ROAD_WIDTH / 4 + 0 * margin, i))
    return turn_points, track_points


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class TestAutonomusTurn:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        # self.turn_points = [(200, 700), (300, 700), (500, 400), (850, 400), (1200, 400)]
        self.turn_points, self.curve_points = get_points()
        self.tree = KDTree(self.curve_points)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.car = Car(
            BasicBrand(),
            Point(50, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
            velocity=0,
        )
        self.background_drafter = IntersectionDrafter(
            self.screen_width, self.screen_height
        )
        self.autonomous_driving = BasicAutonomousDriving(self.car, self.curve_points)
        self.counter = 0

    def draw(self):
        self.background_drafter.draw(self.screen)
        self.car.draw(self.screen)

        for i in range(len(self.curve_points)):
            pygame.draw.circle(
                self.screen,
                (0, 255, 0),
                (self.curve_points[i]),
                5,
            )
        for point in self.turn_points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 5)

        distance, index = self.tree.query(
            [self.car.front_middle.x, self.car.front_middle.y]
        )
        closest_point = self.curve_points[index]
        pygame.draw.circle(self.screen, (0, 0, 255), closest_point, 5)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        point = self.car.front_middle.add_vector(
            self.car.direction.scale(self.car.velocity * self.car.velocity + 10)
        )
        _, index = self.tree.query([point.x, point.y])
        closest_point = self.curve_points[index]
        distance, _ = self.tree.query(closest_point)
        pygame.draw.circle(self.screen, (124, 123, 1), closest_point, 5)
        pygame.draw.circle(self.screen, (255, 123, 1), [point.x, point.y], 5)

    def next_frame(self):
        self.counter += 1
        self.autonomous_driving.move()
        # self.car.move()

    def speed_up_front(self):
        self.car.speed_up(Directions.FRONT)

    def speed_up_reverse(self):
        self.car.speed_up(Directions.BACK)

    def brake(self):
        self.car.brake()

    def turn_left(self):
        self.car.turn(Directions.LEFT)

    def turn_right(self):
        self.car.turn(Directions.RIGHT)


pygame.init()
clock = pygame.time.Clock()
game = TestAutonomusTurn()

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
    clock.tick(30)
