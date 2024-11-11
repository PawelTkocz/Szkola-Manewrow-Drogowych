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
                self.car_simulation.move()  # z jakiegos powodu w tym miejscu zmienia sie wartosc w start_state.body.front_left
                res = self.evaluate_situation(self.car_simulation)
                if min_res is None or res < min_res:
                    best_wheels_modification_index = wheels_modification_index
                    best_speed_modification_index = speed_modification_index
                    min_res = res
                self.car_simulation.set_state(start_state)

        print(
            self.turn_options_description[best_wheels_modification_index],
            self.speed_options_description[best_speed_modification_index],
            self.car_simulation.velocity,
        )
        self.apply_modifications(
            "real_car", best_wheels_modification_index, best_speed_modification_index
        )
        # print(self.car.body.front_left.x, self.car.body.front_left.y)
        # print(self.car.body.front_right.x, self.car.body.front_right.y)
        # print(self.car.body.rear_left.x, self.car.body.rear_left.y)
        # print(self.car.body.rear_right.x, self.car.body.rear_right.y)
        self.car.move()

        self.apply_modifications(
            "simulation_car",
            best_wheels_modification_index,
            best_speed_modification_index,
        )
        self.car_simulation.move()

    def evaluate_situation(self, car: Car):
        distance, index = self.tree.query([car.front_left.x, car.front_left.y])
        # print(distance, car.front_left.x, car.front_left.y)

        velocity = (car.max_velocity - car.velocity) * 100
        return distance * 50 + velocity
