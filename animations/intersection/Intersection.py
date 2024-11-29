import math

from Geometry import Direction, Directions, Point, Vector
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

vertical = [Directions.UP, Directions.DOWN]
horizontal = [Directions.LEFT, Directions.RIGHT]

intersection = {
    "start_roads": {
        Directions.LEFT: {
            "point": Point(
                SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4
            ),
            "direction": Direction(Point(1, 0)),
        },
        Directions.UP: {
            "point": Point(
                SCREEN_WIDTH / 2 - ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2
            ),
            "direction": Direction(Point(0, 1)),
        },
        Directions.RIGHT: {
            "point": Point(
                SCREEN_WIDTH / 2 + ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4
            ),
            "direction": Direction(Point(-1, 0)),
        },
        Directions.DOWN: {
            "point": Point(
                SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2
            ),
            "direction": Direction(Point(0, -1)),
        },
    },
    "end_roads": {
        Directions.LEFT: {
            "point": Point(
                SCREEN_WIDTH / 2 - ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 4
            ),
            "direction": Direction(Point(-1, 0)),
        },
        Directions.UP: {
            "point": Point(
                SCREEN_WIDTH / 2 + ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2
            ),
            "direction": Direction(Point(0, -1)),
        },
        Directions.RIGHT: {
            "point": Point(
                SCREEN_WIDTH / 2 + ROAD_WIDTH / 2, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4
            ),
            "direction": Direction(Point(1, 0)),
        },
        Directions.DOWN: {
            "point": Point(
                SCREEN_WIDTH / 2 - ROAD_WIDTH / 4, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 2
            ),
            "direction": Direction(Point(0, 1)),
        },
    },
}


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


def get_horizontal_track(p: Point):
    margin = 1000
    return [(x, p.y) for x in range(-1 * margin, SCREEN_WIDTH + margin)]


def get_vertical_track(p: Point):
    margin = 1000
    return [(p.x, y) for y in range(-1 * margin, SCREEN_HEIGHT + margin)]


def get_straight_track(start_point: Point, end_point: Point):
    x1, y1 = start_point.x, start_point.y
    x2, y2 = end_point.x, end_point.y
    number_of_points = max(abs(x2 - x1), abs(y2 - y1)) + 1
    x_values = np.linspace(x1, x2, int(number_of_points))
    y_values = np.linspace(y1, y2, int(number_of_points))
    return list(zip(x_values, y_values))


def get_turn_track(start_side: Directions, end_side: Directions, turn_points_vectors):
    start_intersection_point = intersection["start_roads"][start_side]["point"]
    end_intersection_point = intersection["end_roads"][end_side]["point"]
    start_intersection_direction = intersection["start_roads"][start_side]["direction"]
    end_intersection_direction = intersection["end_roads"][end_side]["direction"]

    road_screen_margin = 1000

    start_turn_point = start_intersection_point.copy().add_vector(
        turn_points_vectors[0]
    )
    start_track_length = (
        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2 + road_screen_margin
        if start_side in vertical
        else SCREEN_WIDTH / 2 - ROAD_WIDTH / 2 + road_screen_margin
    )
    start_track_point = start_intersection_point.copy().add_vector(
        start_intersection_direction.get_negative_of_a_vector().scale_to_len(
            start_track_length
        )
    )
    start_track_line = get_straight_track(start_track_point, start_turn_point)

    end_turn_point = end_intersection_point.copy().add_vector(turn_points_vectors[3])
    end_track_length = (
        SCREEN_HEIGHT / 2 - ROAD_WIDTH / 2 + road_screen_margin
        if end_side in vertical
        else SCREEN_WIDTH / 2 - ROAD_WIDTH / 2 + road_screen_margin
    )
    end_track_point = end_intersection_point.copy().add_vector(
        end_intersection_direction.copy().scale_to_len(end_track_length)
    )
    end_track_line = get_straight_track(end_turn_point, end_track_point)

    second_turn_point = start_intersection_point.copy().add_vector(
        turn_points_vectors[1]
    )
    third_turn_point = end_intersection_point.copy().add_vector(turn_points_vectors[2])
    turn_points = [
        (start_turn_point.x, start_turn_point.y),
        (second_turn_point.x, second_turn_point.y),
        (third_turn_point.x, third_turn_point.y),
        (end_turn_point.x, end_turn_point.y),
    ]
    p0, p1, p2, p3 = turn_points
    turn_track_points = [
        cubic_bezier(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 200)
    ]

    start_track_line.extend(turn_track_points)
    start_track_line.extend(end_track_line)
    return turn_points, start_track_line


def get_short_turn_track(start_side: Directions, end_side: Directions):
    margin = 180  # car length ?
    start_intersection_direction = intersection["start_roads"][start_side]["direction"]
    end_intersection_direction = intersection["end_roads"][end_side]["direction"]

    start_turn_vector = (
        start_intersection_direction.get_negative_of_a_vector().scale_to_len(margin)
    )
    second_point_vector = start_intersection_direction.copy().scale_to_len(
        ROAD_WIDTH / 8 + margin * 0.2
    )
    third_point_vector = (
        end_intersection_direction.get_negative_of_a_vector()
        .scale_to_len(ROAD_WIDTH / 8)
        .add_vector(start_intersection_direction.copy().scale_to_len(0.2 * margin))
    )
    end_turn_vector = (
        end_intersection_direction.copy()
        .scale_to_len(margin)
        .add_vector(start_intersection_direction.copy().scale_to_len(0.2 * margin))
    )
    return get_turn_track(
        start_side,
        end_side,
        [start_turn_vector, second_point_vector, third_point_vector, end_turn_vector],
    )


def get_long_turn_track(start_side: Directions, end_side: Directions):
    start_intersection_direction = intersection["start_roads"][start_side]["direction"]
    end_intersection_direction = intersection["end_roads"][end_side]["direction"]

    start_turn_vector = Vector(Point(0, 0))
    second_point_vector = start_intersection_direction.copy().scale_to_len(
        ROAD_WIDTH / 2
    )
    third_point_vector = (
        end_intersection_direction.get_negative_of_a_vector().scale_to_len(
            ROAD_WIDTH / 2
        )
    )
    end_turn_vector = Vector(Point(0, 0))
    return get_turn_track(
        start_side,
        end_side,
        [start_turn_vector, second_point_vector, third_point_vector, end_turn_vector],
    )


def get_track_points(start_side: Directions, end_side: Directions):
    if start_side in vertical and end_side in vertical:
        return [], get_vertical_track(intersection["start_roads"][start_side]["point"])
    if start_side in horizontal and end_side in horizontal:
        return [], get_horizontal_track(
            intersection["start_roads"][start_side]["point"]
        )

    directions = [Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT]
    start_index = directions.index(start_side)
    end_index = directions.index(end_side)
    diff = (end_index - start_index) % 4
    if diff == 1:
        return get_long_turn_track(start_side, end_side)
    if diff == 3:
        return get_short_turn_track(start_side, end_side)

    return []


def prepare_car_ride(
    start_side: Directions, end_side: Directions, distance_to_intersection
):
    start_intersection_point = intersection["start_roads"][start_side]["point"]
    start_intersection_direction = intersection["start_roads"][start_side]["direction"]
    start_position = start_intersection_point.copy().add_vector(
        start_intersection_direction.get_negative_of_a_vector().scale_to_len(
            distance_to_intersection
        )
    )
    _, track_points = get_track_points(start_side, end_side)
    return (
        start_position,
        start_intersection_direction,
        track_points,
    )


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class Intersection:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        directions = [Directions.LEFT, Directions.UP, Directions.RIGHT, Directions.DOWN]
        self.cars = []
        self.autonomous_drivings = []
        for start in directions:
            for end in directions:
                if start == end:
                    continue
                start_position, direction, track_points = prepare_car_ride(
                    start, end, 1000
                )
                car = Car(BasicBrand(), start_position, direction)
                self.cars.append(car)
                autonomous_driving = BasicAutonomousDriving(car, track_points)
                self.autonomous_drivings.append(autonomous_driving)

        # self.turn_points, self.curve_points = get_track_points(
        #     Directions.LEFT, Directions.RIGHT
        # )
        # self.tree = KDTree(self.curve_points)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # self.car = Car(
        #     BasicBrand(),
        #     Point(50, SCREEN_HEIGHT / 2 + ROAD_WIDTH / 4),
        #     velocity=0,
        # )
        self.background_drafter = IntersectionDrafter(
            self.screen_width, self.screen_height
        )
        # self.autonomous_driving = BasicAutonomousDriving(self.car, self.curve_points)
        self.counter = 0

    def draw(self):
        self.background_drafter.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)

        # for i in range(len(self.curve_points)):
        #     pygame.draw.circle(
        #         self.screen,
        #         (0, 255, 0),
        #         (self.curve_points[i]),
        #         1,
        #     )
        # for point in self.turn_points:
        #     pygame.draw.circle(self.screen, (255, 0, 0), point, 5)

        # distance, index = self.tree.query(
        #     [self.car.front_middle.x, self.car.front_middle.y]
        # )
        # closest_point = self.curve_points[index]
        # pygame.draw.circle(self.screen, (0, 0, 255), closest_point, 5)

        # font = pygame.font.Font(None, 36)
        # text = font.render(f"Distance to curve: {int(distance)}", True, (255, 255, 255))
        # self.screen.blit(text, (10, 10))

    def next_frame(self):
        self.counter += 1
        for autonomous_driving in self.autonomous_drivings:
            autonomous_driving.move()
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
game = Intersection()

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
