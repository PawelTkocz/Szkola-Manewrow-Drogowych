import math

from Geometry import Direction, Directions, Point, Rectangle, tuples_list
from animations.constants import SAVED_CAR_MOVEMENT_DIRECTORY
from animations.intersection.IntersectionManoeuvre import IntersectionManoeuvre
from animations.intersection.Manoeuvre import Manoeuvre
from animations.intersection.StreetIntersection import StreetIntersection
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
from autonomousDriving.BasicAutonomousDriving import (
    BasicAutonomousDriving,
)
from cars.BasicBrand import BasicBrand
from cars.Car import Car, SpeedModifications
import os

import pygame


# if it will still be lagging i can do sth like computation of max velocities for each point on the line before the animation starts
class Intersection:
    saved_car_movement_directory = "Intersection"

    def __init__(self, read_movement_from_file: bool, directory_name: str):
        self.cars = []
        self.starting_site = []
        self.ending_site = []
        self.preferences_directions = []
        self.preferences_cars = []
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
                        for carIndex in self.preferences_cars[index]
                    ]
                )
            )

    def save_cars_movement(self):
        for index in range(len(self.cars)):
            if not os.path.exists(SAVED_CAR_MOVEMENT_DIRECTORY):
                os.makedirs(SAVED_CAR_MOVEMENT_DIRECTORY)
            intersection_directory = os.path.join(
                SAVED_CAR_MOVEMENT_DIRECTORY, self.saved_car_movement_directory
            )
            if not os.path.exists(intersection_directory):
                os.makedirs(intersection_directory)
            intersection_manoeuvre_directory = os.path.join(
                intersection_directory, self.directory_name
            )
            if not os.path.exists(intersection_manoeuvre_directory):
                os.makedirs(intersection_manoeuvre_directory)
            file_path = os.path.join(
                intersection_manoeuvre_directory, f"car{index+1}.txt"
            )
            with open(file_path, "w") as file:
                for mod in self.movement_histories[index]:
                    file.write(f"{mod[0].name} {mod[1].name}\n")

    def add_car(
        self,
        direction_start: Directions,
        direction_end: Directions,
        distance_to_intersection: int,
        non_preference_zone: Rectangle,
    ):
        brand = BasicBrand()
        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                direction_start, direction_end, distance_to_intersection, brand.length
            )
        )
        car = Car(brand, start_position, direction)
        self.cars.append(car)
        self.starting_site.append(direction_start)
        self.ending_site.append(direction_end)
        self.movement_histories.append([])

        manoeuvre = Manoeuvre(
            [IntersectionManoeuvre(track_points, non_preference_zone)]
        )
        autonomous_driving = BasicAutonomousDriving(car, manoeuvre)
        self.autonomous_drivings.append(autonomous_driving)
        self.calculate_preferences()
        if self.read_movement_from_file:
            file_path = os.path.join(
                SAVED_CAR_MOVEMENT_DIRECTORY,
                self.saved_car_movement_directory,
                self.directory_name,
                f"car{len(self.cars)}.txt",
            )
            with open(file_path, "r") as file:
                self.steps.append([tuple(line.split()) for line in file])

    def calculate_preferences(self):
        starting_site = self.starting_site[-1]
        ending_site = self.ending_site[-1]
        directions = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        starting_site_index = directions.index(starting_site)
        preferences_directions = []
        for i in range(1, 3):
            if directions[(starting_site_index + i) % 4] != ending_site:
                preferences_directions.append(directions[(starting_site_index + i) % 4])
            else:
                break
        self.preferences_directions.append(preferences_directions)
        last_index = len(self.cars) - 1
        for index, preference_list in enumerate(self.preferences_cars):
            if starting_site in self.preferences_directions[index]:
                preference_list.append(last_index)
        self.preferences_cars.append(
            [
                index
                for index in range(last_index)
                if self.starting_site[index] in preferences_directions
            ]
        )
