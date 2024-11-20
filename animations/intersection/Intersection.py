import math

from Geometry import Directions, Point
from animations.intersection.IntersectionDrafter import IntersectionDrafter
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import (
    BasicAutonomousDriving,
)
from cars.BasicBrand import BasicBrand
from cars.Car import Car

import pygame
import numpy as np
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


def get_intersection_start_point(direction: Directions):
    if direction == Directions.DOWN:
        return Point(
            SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2
        )
    if direction == Directions.LEFT:
        return Point(
            SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4
        )
    if direction == Directions.UP:
        return Point(
            SCREEN_WIDTH / 2 - ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2
        )
    if direction == Directions.RIGHT:
        return Point(
            SCREEN_WIDTH / 2 + ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4
        )
    return Point(0, 0)


def get_intersection_end_point(direction: Directions):
    if direction == Directions.DOWN:
        return Point(
            SCREEN_WIDTH / 2 - ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2
        )
    if direction == Directions.LEFT:
        return Point(
            SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4
        )
    if direction == Directions.UP:
        return Point(
            SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2
        )
    if direction == Directions.RIGHT:
        return Point(
            SCREEN_WIDTH / 2 + ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4
        )
    return Point(0, 0)


def get_track_points(start_side: Directions, end_side: Directions):
    pass


def get_short_turn_points():
    """
    Points represent track of turn from left side of the intersection to down side
    """
    margin = 180  # car length ?
    start_intersection_point = get_intersection_start_point(Directions.LEFT)
    end_intersection_point = get_intersection_end_point(Directions.DOWN)
    start_track_line = [
        (x, start_intersection_point.y)
        for x in range(-500, int(start_intersection_point.x) - margin)
    ]

    turn_points = [
        (
            start_intersection_point.x - margin,
            start_intersection_point.y,
        ),
        (
            end_intersection_point.x - ROAD_WIDTH / 8 + margin * 0.2,
            start_intersection_point.y,
        ),
        (
            end_intersection_point.x + margin * 0.2,
            start_intersection_point.y + ROAD_WIDTH / 8,
        ),
        (
            end_intersection_point.x + margin * 0.2,
            end_intersection_point.y + margin,
        ),
    ]
    # print(turn_points)
    p0, p1, p2, p3 = turn_points
    t_values = np.linspace(0, 1, 200)
    curve_points = [cubic_bezier(t, p0, p1, p2, p3) for t in t_values]
    end_track_line = [
        (end_intersection_point.x + margin * 0.2, y)
        for y in range(int(end_intersection_point.y) + margin, SCREEN_HEIGHT + 500)
    ]
    start_track_line.extend(curve_points)
    start_track_line.extend(end_track_line)
    return turn_points, start_track_line
    # to get other turns i can rotate start_track_line over middle of screen


def get_points_left_turn():
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
    for y in range(1, SCREEN_HEIGHT // 2 - ROAD_WIDTH // 2 + 1000):
        track_points.append(
            (
                SCREEN_WIDTH / 2 + ROAD_WIDTH / 4 + 0 * margin,
                SCREEN_HEIGHT // 2 - ROAD_WIDTH // 2 - y,
            )
        )
    return turn_points, track_points


def get_points_straight_track():
    track_points = [
        (x, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4)
        for x in np.linspace(0, SCREEN_WIDTH + 1000, 500)
    ]
    return [], track_points


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class TestAutonomusTurn:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        self.turn_points, self.curve_points = get_points_left_turn()
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
                1,
            )
        for point in self.turn_points:
            pygame.draw.circle(self.screen, (255, 0, 0), point, 5)

        distance, index = self.tree.query(
            [self.car.front_middle.x, self.car.front_middle.y]
        )
        closest_point = self.curve_points[index]
        pygame.draw.circle(self.screen, (0, 0, 255), closest_point, 5)

        _, index = self.tree.query([self.car.front_middle.x, self.car.front_middle.y])
        goal_point_index = (
            self.autonomous_driving.car_simulation.track.furthest_point_indexes_in_line[
                index
            ]
        )
        pygame.draw.circle(
            self.screen, (200, 100, 0), self.curve_points[goal_point_index], 5
        )

        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

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
