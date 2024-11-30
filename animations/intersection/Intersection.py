import math

from Geometry import Direction, Directions, Point, Rectangle
from animations.intersection.IntersectionManoeuvre import IntersectionManoeuvre
from animations.intersection.Manoeuvre import Manoeuvre
from animations.intersection.StreetIntersection import StreetIntersection
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import (
    BasicAutonomousDriving,
)
from cars.BasicBrand import BasicBrand
from cars.Car import Car, SpeedModifications

import pygame

read_movement_from_file = False


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class Intersection:
    screen_height = 800
    screen_width = 1400

    def __init__(self):
        if read_movement_from_file:
            with open("car1.txt", "r") as file:
                self.steps1 = [tuple(line.split()) for line in file]
            with open("car2.txt", "r") as file:
                self.steps2 = [tuple(line.split()) for line in file]

        self.street_intersection = StreetIntersection()

        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                Directions.DOWN, Directions.UP, 700
            )
        )
        self.intersection_manoeuvre1 = Manoeuvre(
            [IntersectionManoeuvre(track_points, None)]
        )
        self.car1 = Car(BasicBrand(), start_position, direction)
        self.autonomous_driving1 = BasicAutonomousDriving(
            self.car1, self.intersection_manoeuvre1
        )
        self.movement_history1 = []

        start_position2, direction2, track_points2 = (
            self.street_intersection.prepare_car_ride(
                Directions.LEFT, Directions.RIGHT, 700
            )
        )
        self.intersection_manoeuvre2 = Manoeuvre(
            [
                IntersectionManoeuvre(
                    track_points2,
                    Rectangle(
                        Point(
                            SCREEN_WIDTH / 2,
                            SCREEN_HEIGHT - (SCREEN_HEIGHT - ROAD_WIDTH) / 2,
                        ),
                        ROAD_WIDTH,
                        ROAD_WIDTH,
                        Direction(Point(0, 1)),
                    ),
                )
            ]
        )
        self.car2 = Car(BasicBrand(), start_position2, direction2)
        self.autonomous_driving2 = BasicAutonomousDriving(
            self.car2, self.intersection_manoeuvre2
        )
        self.movement_history2 = []

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.counter = 0

    def draw(self):
        self.street_intersection.draw(self.screen)
        self.car1.draw(self.screen)
        self.car2.draw(self.screen)

    def next_frame(self):
        if read_movement_from_file:
            if self.counter >= len(self.steps1):
                return
            self.autonomous_driving1.apply_best_changes(
                Directions[self.steps1[self.counter][0]],
                SpeedModifications[self.steps1[self.counter][1]],
            )
            self.autonomous_driving2.apply_best_changes(
                Directions[self.steps2[self.counter][0]],
                SpeedModifications[self.steps2[self.counter][1]],
            )
            self.counter += 1
        else:
            self.movement_history1.append(self.autonomous_driving1.move([]))
            self.movement_history2.append(self.autonomous_driving2.move([]))

    def save_cars_movement(self):
        file1 = "car1.txt"
        file2 = "car2.txt"
        with open(file1, "w") as file:
            for mod in self.movement_history1:
                file.write(f"{mod[0].name} {mod[1].name}\n")
        with open(file2, "w") as file:
            for mod in self.movement_history2:
                file.write(f"{mod[0].name} {mod[1].name}\n")


pygame.init()
clock = pygame.time.Clock()
game = Intersection()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not read_movement_from_file:
                game.save_cars_movement()
            pygame.quit()
            exit()

    game.draw()
    game.next_frame()
    pygame.display.update()
    clock.tick(30)
