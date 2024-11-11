import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree

from Geometry import Directions, Rectangle
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car


class BasicAutonomousDriving:

    turn_options = [Directions.LEFT, Directions.FRONT, Directions.RIGHT]
    turn_options_description = ["turn left", "no turn", "turn right"]
    speed_options_description = ["brake", "speed front", "speed reverse"]

    def __init__(self, car: Car, curve_points):
        self.car = car
        self.curve_points = curve_points
        self.tree = KDTree(self.curve_points)
        self.car_simulation = CarSimulation(
            car.brand, car.front_left, car.direction, car.velocity
        )
        self.wheels_modifications = dict(
            map(
                lambda car_data: (
                    car_data[0],
                    list(
                        map(
                            lambda direction: {
                                "method": car_data[1].turn,
                                "params": [direction],
                            },
                            self.turn_options,
                        )
                    ),
                ),
                [("real_car", self.car), ("simulation_car", self.car_simulation)],
            )
        )
        self.speed_modifications = dict(
            map(
                lambda car_data: (
                    car_data[0],
                    [
                        {"method": car_data[1].brake, "params": []},
                        {"method": car_data[1].speed_up, "params": [Directions.FRONT]},
                        {"method": car_data[1].speed_up, "params": [Directions.BACK]},
                    ],
                ),
                [("real_car", self.car), ("simulation_car", self.car_simulation)],
            )
        )

    def apply_modifications(
        self, car_name, wheels_modification_index, speed_modification_index
    ):
        wheels_modification = self.wheels_modifications[car_name][
            wheels_modification_index
        ]
        wheels_modification["method"](*wheels_modification["params"])
        speed_modification = self.speed_modifications[car_name][
            speed_modification_index
        ]
        speed_modification["method"](*speed_modification["params"])

    def move(self):
        min_res = None
        best_wheels_modification_index = None
        best_speed_modification_index = None
        for wheels_modification_index, wheels_modification in enumerate(
            self.wheels_modifications["simulation_car"]
        ):
            start_state = self.car_simulation.get_state()
            for speed_modification_index, speed_modification in enumerate(
                self.speed_modifications["simulation_car"]
            ):
                wheels_modification["method"](*wheels_modification["params"])
                speed_modification["method"](*speed_modification["params"])
                self.car_simulation.move()
                res = self.evaluate_situation(self.car_simulation)
                if min_res is None or res < min_res:
                    best_wheels_modification_index = wheels_modification_index
                    best_speed_modification_index = speed_modification_index
                    min_res = res
                self.car_simulation.set_state(start_state)

        if best_speed_modification_index != 1:
            print(self.speed_options_description[best_speed_modification_index])

        self.apply_modifications(
            "real_car", best_wheels_modification_index, best_speed_modification_index
        )
        self.car.move()

        self.apply_modifications(
            "simulation_car",
            best_wheels_modification_index,
            best_speed_modification_index,
        )
        self.car_simulation.move()

    def evaluate_velocity_heuristic_points(self, car: Car):
        v = car.velocity
        max_v = car.max_velocity
        value = v / max_v
        # returned value in range [0, 10]
        if value < 0.2:
            return 10 - 30 * value  # [4, 10]
        elif value < 0.7:  # [0.2, 0.7]
            return 4 - 6 * (value - 0.2)  # [1, 4]
        else:  # [0.7, 1]
            return 1 - 10 / 3 * (value - 0.7)  # [0, 1]

    def evaluate_distance_heuristic_points(self, car: Car):
        distance, _ = self.tree.query([car.front_left.x, car.front_left.y])
        value = distance / car.width  # distance in car widths
        if value < 0.1:  # less than 0.1 width
            return 10 * value  # [0, 1]
        elif value < 0.2:  # [0.1 widht, 0.2 width]
            return 1 + 20 * (value - 0.1)  # [1, 3]
        elif value < 0.5:  # [0.2 width, 0.5 widht]
            return 3 + 60 * (value - 0.2)  # [3, 21]
        elif value < 1:  # [0.5 width, 1 width]
            return 21 + 150 * (value - 0.5)  # [21, 96]
        else:  # more than 1 car width
            return 96 + 500 * (value - 1)  # [96, inf]

    def evaluate_situation(self, car: Car):
        # jesli velocity jest jakas mala to moze nie przejmuj sie tak dystansem zeby zachecic do zwiekzenia v
        distance_importance = 5
        velocity_importance = 1
        distance_points = self.evaluate_distance_heuristic_points(car)  # [0, inf]
        velocity_points = self.evaluate_velocity_heuristic_points(car)  # [0, 10]
        return (
            distance_importance * distance_points
            + velocity_importance * velocity_points
        )
