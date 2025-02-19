from typing import TypedDict
from geometry import Directions, Rectangle
from animations.constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as general_car_movement_directory,
)
from animations.intersection.constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as intersection_car_movement_directory,
)
from animations.intersection.intersection_manoeuvre import IntersectionManoeuvre
from animations.intersection.manoeuvre import Manoeuvre
from animations.intersection.street_intersection import StreetIntersection
from autonomousDriving.basic_autonomous_driving import (
    BasicAutonomousDriving,
)
from car.car import Car, SpeedModifications
import os

from car.toyota_yaris import ToyotaYaris


class IntersectionCarInfo(TypedDict):
    id: int  # car id
    car: Car  # car instance
    autonomous_driving: BasicAutonomousDriving  # autonomous driving instance
    starting_site: (
        Directions  # site of the intersection where the car starts its movement
    )
    ending_site: Directions  # site of the intersection where the car ends its movement
    sites_with_preference: list[
        Directions
    ]  # list of intersection sites which have preference during this manoeuvre
    cars_with_preference: list[
        "IntersectionCarInfo"
    ]  # list of cars which have preference during this manoeuvre
    movement_history: list[tuple[Directions, SpeedModifications]]  # movement history


class Intersection:
    def __init__(self, read_movement_from_file: bool, directory_name: str):

        self.cars_info: list[IntersectionCarInfo] = []
        self.read_movement_from_file = read_movement_from_file
        self.directory_name = directory_name
        self.street_intersection = StreetIntersection()
        self.counter = 0

    def draw(self, screen):
        self.street_intersection.draw(screen)
        for car in [car_info["car"] for car_info in self.cars_info]:
            car.draw(screen)

    def move(self):
        if self.read_movement_from_file:
            for car_info in self.cars_info:
                if self.counter >= len(car_info["movement_history"]):
                    return
                car_info["autonomous_driving"].apply_best_changes(
                    Directions[car_info["movement_history"][self.counter][0]],
                    SpeedModifications[car_info["movement_history"][self.counter][1]],
                )
            self.counter += 1
            return

        for car_info in self.cars_info:
            car_info["movement_history"].append(
                car_info["autonomous_driving"].move(
                    [
                        car_with_preference["autonomous_driving"].car_simulation
                        for car_with_preference in car_info["cars_with_preference"]
                    ]
                )
            )

    def save_cars_movement(self):
        for car_info in self.cars_info:
            if not os.path.exists(general_car_movement_directory):
                os.makedirs(general_car_movement_directory)
            intersection_directory = os.path.join(
                general_car_movement_directory, intersection_car_movement_directory
            )
            if not os.path.exists(intersection_directory):
                os.makedirs(intersection_directory)
            intersection_manoeuvre_directory = os.path.join(
                intersection_directory, self.directory_name
            )
            if not os.path.exists(intersection_manoeuvre_directory):
                os.makedirs(intersection_manoeuvre_directory)
            car_id = car_info["id"]
            file_path = os.path.join(
                intersection_manoeuvre_directory, f"car{car_id}.txt"
            )
            with open(file_path, "w") as file:
                for mod in car_info["movement_history"]:
                    file.write(f"{mod[0].name} {mod[1].name}\n")

    def add_car(
        self,
        direction_start: Directions,
        direction_end: Directions,
        distance_to_intersection: int,
        non_preference_zone: Rectangle,
    ):
        model = ToyotaYaris()
        start_position, direction, track_points = (
            self.street_intersection.prepare_car_ride(
                direction_start, direction_end, distance_to_intersection, model.length
            )
        )
        car = Car(model, "red", start_position, direction)
        manoeuvre = Manoeuvre(
            [IntersectionManoeuvre(track_points, non_preference_zone)]
        )

        car_info = {
            "id": len(self.cars_info) + 1,
            "car": car,
            "starting_site": direction_start,
            "ending_site": direction_end,
            "movement_history": [],
            "autonomous_driving": BasicAutonomousDriving(car, manoeuvre),
            "sites_with_preference": self.calculate_sites_with_preference(
                direction_start, direction_end
            ),
            "cars_with_preference": [],
        }
        # calculate non preference zone

        if self.read_movement_from_file:
            car_info["movement_history"] = self.get_car_movement(car_info["id"])

        self.cars_info.append(car_info)
        self.calculate_cars_with_preference(car_info)

    def calculate_sites_with_preference(self, starting_site, ending_site):
        directions = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        starting_site_index = directions.index(starting_site)
        preferences_directions = []
        for i in range(1, 3):
            if directions[(starting_site_index + i) % 4] != ending_site:
                preferences_directions.append(directions[(starting_site_index + i) % 4])
            else:
                break
        return preferences_directions

    def calculate_cars_with_preference(self, car_info: IntersectionCarInfo):
        starting_site = car_info["starting_site"]

        # update cars_with_preference for other cars if they have to give preference to car_info
        for intersection_car in self.cars_info:
            if (
                intersection_car is not car_info
                and starting_site in intersection_car["sites_with_preference"]
            ):
                intersection_car["cars_with_preference"].append(car_info)

        # set cars_with_preference for car_info
        car_info["cars_with_preference"] = [
            intersection_car
            for intersection_car in self.cars_info
            if intersection_car is not car_info
            and intersection_car["starting_site"] in car_info["sites_with_preference"]
        ]

    def get_car_movement(self, car_id):
        file_path = os.path.join(
            general_car_movement_directory,
            intersection_car_movement_directory,
            self.directory_name,
            f"car{car_id}.txt",
        )
        movement_history = []
        with open(file_path, "r") as file:
            movement_history.extend([tuple(line.split()) for line in file])
        return movement_history
