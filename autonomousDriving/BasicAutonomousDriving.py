import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree

from Geometry import Directions, Rectangle
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car
from drawing.utils import tuples_list


# zmiana planow
# zamiast funkcji heurystycznej zrobic tak:
# kierunek skretu definiujemy symulujac trzy sytuacje: lewo, prawo, bez skretu (z predkoscia obecna) i patrzymy gdzie odleglosc jest najmniejsza
# znajac kierunek skretu trzeba jeszcze dobrac zmiane predkosci: rowniez symulujemy sytuacje: przyspiesz, bez zmian, hamuj. Przemiesc sie do przodu i sprawdz,
# czy wykonujac n krokow postaci "skrec w opdowiednia strone i hamuj" jestes w stanie nie przekroczyc w żadnym kroku pewnego maksymalnego dystansu od krzywej.
# Jesli tak to okej, jesli nie to rozwaz wolniejsza opcje.
class BasicAutonomousDriving:
    def __init__(self, car: Car, curve_points):
        self.car = car
        self.curve_points = curve_points
        self.tree = KDTree(self.curve_points)
        self.car_simulation = CarSimulation(
            car.brand, car.front_left, car.direction, car.velocity
        )
        self.max_distance_to_track = 20
        self.steps_into_the_future = 30
        self.wheels_modifications = {
            "turn_left": {
                "real_car_method": self.car.turn,
                "simulation_car_method": self.car_simulation.turn,
                "params": [Directions.LEFT],
            },
            "go_straight": {
                "real_car_method": self.car.turn,
                "simulation_car_method": self.car_simulation.turn,
                "params": [Directions.FRONT],
            },
            "turn_right": {
                "real_car_method": self.car.turn,
                "simulation_car_method": self.car_simulation.turn,
                "params": [Directions.RIGHT],
            },
        }
        self.speed_modifications = {
            "brake": {
                "real_car_method": self.car.brake,
                "simulation_car_method": self.car_simulation.brake,
                "params": [],
            },
            "speed_front": {
                "real_car_method": self.car.speed_up,
                "simulation_car_method": self.car_simulation.speed_up,
                "params": [Directions.FRONT],
            },
            "speed_reverse": {
                "real_car_method": self.car.speed_up,
                "simulation_car_method": self.car_simulation.speed_up,
                "params": [Directions.BACK],
            },
        }

    def find_best_wheels_modification(self, prints=False):
        min_distance = None
        best_wheels_modification = None
        for wheels_modification_name in self.wheels_modifications:
            start_state = self.car_simulation.get_state()
            wheels_modification = self.wheels_modifications[wheels_modification_name]
            wheels_modification["simulation_car_method"](*wheels_modification["params"])
            self.car_simulation.move()
            distance = self.find_distance(self.car_simulation)
            if prints:
                print(wheels_modification_name, distance)
            if min_distance is None or distance < min_distance:
                best_wheels_modification = wheels_modification_name
                min_distance = distance
            self.car_simulation.set_state(start_state)
        return best_wheels_modification

    def will_go_off_track(self):
        if self.find_distance(self.car_simulation) > self.max_distance_to_track:
            return True
        start_state = self.car_simulation.get_state()
        went_off_track = False
        for _ in range(self.steps_into_the_future):
            self.car_simulation.brake()
            best_wheels_modification_name = self.find_best_wheels_modification()
            best_wheels_modification = self.wheels_modifications[
                best_wheels_modification_name
            ]
            best_wheels_modification["simulation_car_method"](
                *best_wheels_modification["params"]
            )
            self.car_simulation.move()
            if self.find_distance(self.car_simulation) > self.max_distance_to_track:
                went_off_track = True
                break
            if self.car_simulation.velocity == 0:
                break
        self.car_simulation.set_state(start_state)
        return went_off_track

    def find_best_speed_modification(self, best_wheels_modification_name):
        speed_modification_names = (
            ["speed_front", "speed_reverse", "brake"]
            if self.car_simulation.velocity >= 0
            else ["speed_reverse", "speed_front", "brake"]
        )
        for speed_modification_name in speed_modification_names:
            speed_modification = self.speed_modifications[speed_modification_name]
            best_wheels_modification = self.wheels_modifications[
                best_wheels_modification_name
            ]
            start_state = self.car_simulation.get_state()
            speed_modification["simulation_car_method"](*speed_modification["params"])
            best_wheels_modification["simulation_car_method"](
                *best_wheels_modification["params"]
            )
            self.car_simulation.move()
            will_go_off_track = self.will_go_off_track()
            self.car_simulation.set_state(start_state)
            if not will_go_off_track:
                return speed_modification_name
        return "brake"

    def print_car_position(self, car: Car):
        corners = car.body.corners_list
        print(
            tuples_list(corners),
            car.velocity,
            car.direction.x,
            car.direction.y,
            car.wheels.angle,
        )

    def move(self):
        # z jakiegos powodu po jakims czasie zastosowywanie analogicznych zmian w predkosci i skrecaniu dla car i car_simulation
        # ich wspolrzedne corners zaczynaja sie roznic na ostatnich cyfrach po przecinku (np 10) wiec byc moze warto kopiowac a
        # nie zakladac ze zawsze beda rowne
        best_wheels_modification_name = self.find_best_wheels_modification()
        best_speed_modification_name = self.find_best_speed_modification(
            best_wheels_modification_name
        )
        # print(best_wheels_modification_name, best_speed_modification_name)
        best_wheels_modification = self.wheels_modifications[
            best_wheels_modification_name
        ]
        best_wheels_modification["simulation_car_method"](
            *best_wheels_modification["params"]
        )
        best_speed_modification = self.speed_modifications[best_speed_modification_name]
        best_speed_modification["simulation_car_method"](
            *best_speed_modification["params"]
        )
        self.car_simulation.move()

        best_wheels_modification["real_car_method"](*best_wheels_modification["params"])
        best_speed_modification["real_car_method"](*best_speed_modification["params"])
        self.car.move()

    def find_distance(self, car: Car):
        distance, _ = self.tree.query([car.front_left.x, car.front_left.y])
        return distance
