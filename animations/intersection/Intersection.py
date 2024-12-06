import math

from Geometry import Direction, Directions, Point, Rectangle, tuples_list
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


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class Intersection:
    def __init__(self, read_movement_from_file: bool, directory_name: str):
        self.cars = []
        self.preferences = []
        self.autonomous_drivings = []
        self.movement_histories = []
        self.steps = []
        self.read_movement_from_file = read_movement_from_file
        self.directory_name = directory_name
        self.street_intersection = StreetIntersection()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.counter = 0

    def draw(self):
        self.street_intersection.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)

    def move(self):
        if self.read_movement_from_file:
            for index, autonomous_driving in enumerate(self.autonomous_drivings):
                if self.counter >= len(self.steps[index]):
                    return
                autonomous_driving.apply_best_changes(
                    Directions[self.steps[index][self.counter][0]],
                    SpeedModifications[self.steps[index][self.counter][1]],
                )
            self.counter += 1
            return
        for index, autonomous_driving in enumerate(self.autonomous_drivings):
            self.movement_histories[index].append(
                autonomous_driving.move(
                    [
                        self.autonomous_drivings[carIndex].car_simulation
                        for carIndex in self.preferences[index]
                    ]
                )
            )

    def save_cars_movement(self):
        for index in range(len(self.cars)):
            file_name = f"car{index+1}.txt"
            with open(file_name, "w") as file:
                for mod in self.movement_histories[index]:
                    file.write(f"{mod[0].name} {mod[1].name}\n")

    def add_car(
        self,
        direction_start: Directions,
        direction_end: Directions,
        distance_to_intersection: int,
        non_preference_zone: Rectangle,
        preferences: list[int],
    ):
        brand = BasicBrand()
        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                direction_start, direction_end, distance_to_intersection, brand.length
            )
        )
        car = Car(brand, start_position, direction)
        self.cars.append(car)
        self.movement_histories.append([])

        manoeuvre = Manoeuvre(
            [IntersectionManoeuvre(track_points, non_preference_zone)]
        )
        autonomous_driving = BasicAutonomousDriving(car, manoeuvre)
        self.autonomous_drivings.append(autonomous_driving)
        self.preferences.append(preferences)
        if self.read_movement_from_file:
            with open(f"car{len(self.cars)}.txt", "r") as file:
                self.steps.append([tuple(line.split()) for line in file])
