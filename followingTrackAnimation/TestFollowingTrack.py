import math

from Geometry import Directions, Point
from animations.intersection.IntersectionDrafter import IntersectionDrafter
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import (
    BasicAutonomousDriving,
    closest_to_track_turning_policy,
    straight_lines_turning_policy,
)
from autonomousDriving.CarSimulation import CarSimulation
from autonomousDriving.CarSimulation2 import CarSimulation2
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
        self.show_future = False
        self.counter = 0
        self.future_animation_started = False

        self.turn_points, self.curve_points = get_points_left_turn()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.car = Car(
            BasicBrand(),
            Point(50, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
            velocity=0,
        )
        self.future_car_simulation = CarSimulation2(self.car, self.curve_points)
        self.background_drafter = IntersectionDrafter(
            self.screen_width, self.screen_height
        )
        self.autonomous_driving = BasicAutonomousDriving(self.car, self.curve_points)

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

        distance = self.autonomous_driving.car_simulation.find_distance_to_track()
        index = (
            self.autonomous_driving.car_simulation.find_index_of_closest_point_on_track()
        )
        goal_point = self.autonomous_driving.car_simulation.find_straight_line_end_point_on_track(
            index
        )
        pygame.draw.circle(self.screen, (200, 100, 0), goal_point, 5)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def next_frame(self):
        if self.show_future == False:
            self.autonomous_driving.move()
        else:
            if self.future_animation_started:
                turn_direction = closest_to_track_turning_policy(
                    self.future_car_simulation
                )
                self.future_car_simulation.turn(turn_direction)
                self.future_car_simulation.move()
                self.future_car_simulation.draw(self.screen)
                if self.future_car_simulation.velocity == 0:
                    self.show_future = False
                    self.future_animation_started = False

                closest_point_on_track_index = (
                    self.future_car_simulation.find_index_of_closest_point_on_track()
                )
                straight_line_end_point = (
                    self.future_car_simulation.find_straight_line_end_point_on_track(
                        closest_point_on_track_index
                    )
                )
                distance = self.future_car_simulation.find_distance_to_point(
                    straight_line_end_point
                )
                font = pygame.font.Font(None, 36)
                text = font.render(
                    f"Distance: {int(distance)} ({straight_line_end_point[0]}, {straight_line_end_point[1]})",
                    True,
                    (255, 255, 255),
                )
                self.screen.blit(text, (10, 10))

            else:
                self.show_future = True
                self.future_car_simulation.set_state(
                    self.autonomous_driving.car_simulation.get_state()
                )
                self.future_animation_started = True
        # self.car.move()


pygame.init()
clock = pygame.time.Clock()
game = TestAutonomusTurn()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game.next_frame()
    elif keys[pygame.K_DOWN]:
        # game.speed_up_reverse()
        game.show_future = True
        game.next_frame()

    # game.next_frame()
    pygame.display.update()
    clock.tick(30)
