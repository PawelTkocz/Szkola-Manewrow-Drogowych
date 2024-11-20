import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree

from Geometry import Directions, Rectangle, calculate_line, distance_of_point_to_line
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car
from drawing.utils import tuples_list


def calculate_furthest_point_index_in_line_fast(
    track_points: list[tuple[float, float]], start_index, max_distance
):
    curve_points_number = len(track_points)
    if start_index > curve_points_number:
        return start_index

    start_point = track_points[start_index]
    max_end_index = start_index  # najwiekszy t.z wiemy ze dziala

    furthers_possible = curve_points_number - 1  # ostatni ktory moze dzialac
    while max_end_index != furthers_possible:
        end_index = (max_end_index + furthers_possible + 1) // 2
        end_point = track_points[end_index]
        a, b, c = calculate_line(start_point, end_point)

        all_points_in_line = True
        for i in range(start_index + 1, end_index):
            if distance_of_point_to_line(track_points[i], a, b, c) > max_distance:
                all_points_in_line = False
                break

        if not all_points_in_line:
            furthers_possible = end_index - 1
        else:
            max_end_index = end_index
    diff = max_end_index - start_index
    if diff > 180:
        return start_index + 180
    return max_end_index


# problem jest taki ze jak auto jest startowo ustawione to skrecajac w lewo lub prawo przesunie sie na osi x bardziej w prawo niz jadac prosto
# jak to jest mozliwe?


# def calculate_furthest_point_index_in_line(
#     track_points: list[tuple[float, float]], start_index, max_distance
# ):
#     # print(start_index)
#     curve_points_number = len(track_points)
#     if start_index > curve_points_number:
#         return start_index

#     start_point = track_points[start_index]
#     max_end_index = start_index
#     # furthers_fail = curve_points_number - 1
#     # while max_end_index != curve_points_number - 1:
#     #     end_index = (max_end_index + curve_points_number) / 2
#     for end_index in range(start_index + 1, curve_points_number):
#         end_point = track_points[end_index]
#         a, b, c = calculate_line(start_point, end_point)

#         all_points_in_line = True
#         for i in range(start_index + 1, end_index):
#             if distance_of_point_to_line(track_points[i], a, b, c) > max_distance:
#                 all_points_in_line = False
#                 break

#         if not all_points_in_line:
#             break

#         max_end_index = end_index
#     print(start_index, max_end_index)
#     return max_end_index


def calculate_furthest_point_indexes_in_line(
    track_points: list[tuple[float, float]], max_distance
):
    res = []
    jump = 2 * max_distance
    res.append(
        calculate_furthest_point_index_in_line_fast(track_points, 0, max_distance)
    )
    cur_index = 0  # indeks ostatniego uzupelnionego
    while cur_index < len(track_points) - 1:
        jump_index = min(cur_index + jump, len(track_points) - 1)
        furthes_point_index = calculate_furthest_point_index_in_line_fast(
            track_points, jump_index, max_distance
        )
        if furthes_point_index == res[cur_index]:
            for i in range(cur_index + 1, jump_index + 1):
                res.append(res[-1])
        else:
            for i in range(cur_index + 1, jump_index + 1):
                res.append(
                    calculate_furthest_point_index_in_line_fast(
                        track_points, i, max_distance
                    )
                )
        cur_index = jump_index
    return res


# zmiana planow
# zamiast funkcji heurystycznej zrobic tak:
# kierunek skretu definiujemy symulujac trzy sytuacje: lewo, prawo, bez skretu (z predkoscia obecna) i patrzymy gdzie odleglosc jest najmniejsza
# znajac kierunek skretu trzeba jeszcze dobrac zmiane predkosci: rowniez symulujemy sytuacje: przyspiesz, bez zmian, hamuj. Przemiesc sie do przodu i sprawdz,
# czy wykonujac n krokow postaci "skrec w opdowiednia strone i hamuj" jestes w stanie nie przekroczyc w żadnym kroku pewnego maksymalnego dystansu od krzywej.
# Jesli tak to okej, jesli nie to rozwaz wolniejsza opcje.
class BasicAutonomousDriving:
    def __init__(self, car: Car, curve_points: list[tuple[float, float]]):
        self.car = car
        self.curve_points = curve_points
        self.max_distance_to_line = 5
        self.furthest_point_indexes_in_line = calculate_furthest_point_indexes_in_line(
            self.curve_points, self.max_distance_to_line
        )
        self.tree = KDTree(self.curve_points)
        self.car_simulation = CarSimulation(
            car.brand, car.front_middle, car.direction, car.velocity
        )
        self.max_distance_to_track = 100
        self.steps_into_the_future = 30
        self.wheels_modifications = {
            "go_straight": {
                "real_car_method": self.car.turn,
                "simulation_car_method": self.car_simulation.turn,
                "params": [Directions.FRONT],
            },
            "turn_left": {
                "real_car_method": self.car.turn,
                "simulation_car_method": self.car_simulation.turn,
                "params": [Directions.LEFT],
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
        _, index = self.tree.query(
            [self.car_simulation.front_middle.x, self.car_simulation.front_middle.y]
        )
        goal_point_index = self.furthest_point_indexes_in_line[index]
        for wheels_modification_name in self.wheels_modifications:
            start_state = self.car_simulation.get_state()
            wheels_modification = self.wheels_modifications[wheels_modification_name]
            wheels_modification["simulation_car_method"](*wheels_modification["params"])
            self.car_simulation.move()
            # distance = self.find_distance_heuristic(self.car_simulation)
            # distance = self.find_distance_to_track(self.car_simulation)
            distance = self.find_distance_to_point(
                self.car_simulation, self.curve_points[goal_point_index]
            )
            if prints:
                print(
                    wheels_modification_name,
                    distance,
                    self.car_simulation.front_middle.x,
                    self.car_simulation.front_middle.y,
                )
            if min_distance is None or distance < min_distance:
                best_wheels_modification = wheels_modification_name
                min_distance = distance
            self.car_simulation.set_state(start_state)
        return best_wheels_modification

    def will_go_off_track(self):
        if (
            self.find_distance_to_track(self.car_simulation)
            > self.max_distance_to_track
        ):
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
            if (
                self.find_distance_to_track(self.car_simulation)
                > self.max_distance_to_track
            ):
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
            # print(speed_modification_name, will_go_off_track)
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
        # print(
        #     best_wheels_modification_name,
        #     best_speed_modification_name,
        #     self.car.front_middle.x,
        #     self.car.front_middle.y,
        #     end="\n\n",
        # )
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

    # def find_distance_heuristic(self, car: Car):
    #     distance, index = self.tree.query([car.front_middle.x, car.front_middle.y])
    #     closest_point = self.curve_points[index]
    #     x1, y1 = closest_point[0], closest_point[1]
    #     x2, y2 = car.front_middle.x, car.front_middle.y
    #     return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def find_distance_to_track(self, car: Car):
        distances, _ = self.tree.query([car.front_middle.x, car.front_middle.y], k=2)
        return distances[0] + distances[1]

    def find_distance_to_point(self, car: Car, point):
        x1, y1 = point[0], point[1]
        x2, y2 = car.front_middle.x, car.front_middle.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
