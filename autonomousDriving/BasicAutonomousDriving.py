import math
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree

from Geometry import Directions, Rectangle, calculate_line, distance_of_point_to_line
from animations.intersection.constants import ROAD_WIDTH, SCREEN_HEIGHT
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car, SpeedModifications
from drawing.utils import tuples_list


def basic_turning_policy(car_simulation: CarSimulation):
    min_distance = None
    best_turn_direction = None

    closest_point_on_track_index = car_simulation.find_index_of_closest_point_on_track()
    straight_line_end_point = car_simulation.find_straight_line_end_point_on_track(
        closest_point_on_track_index
    )

    for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
        start_state = car_simulation.get_state()
        car_simulation.turn(turn_direction)
        car_simulation.move()
        distance = car_simulation.find_distance_to_point(straight_line_end_point)
        if min_distance is None or distance < min_distance:
            best_turn_direction = turn_direction
            min_distance = distance
        car_simulation.set_state(start_state)

    return best_turn_direction


class BasicAutonomousDriving:
    def __init__(self, car: Car, track: list[tuple[float, float]]):
        self.car = car
        self.track = track
        self.car_simulation = CarSimulation(car, track)
        self.turning_policy = basic_turning_policy
        self.max_distance_to_track = 50
        self.max_steps_into_future = 100  # 340 max speed / resistance

    def find_best_speed_modification(self):
        for speed_modification in [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]:
            start_state = self.car_simulation.get_state()
            self.car_simulation.apply_speed_modification(speed_modification)
            self.car_simulation.move()
            will_go_off_track = self.car_simulation.will_go_off_track(
                self.max_distance_to_track,
                self.max_steps_into_future,
                basic_turning_policy,
                None,
            )
            self.car_simulation.set_state(start_state)
            if not will_go_off_track:
                return speed_modification
        return SpeedModifications.BRAKE

    def move(self):
        # z jakiegos powodu po jakims czasie zastosowywanie analogicznych zmian w predkosci i skrecaniu dla car i car_simulation
        # ich wspolrzedne corners zaczynaja sie roznic na ostatnich cyfrach po przecinku (np 10) wiec byc moze warto kopiowac a
        # nie zakladac ze zawsze beda rowne
        best_turn_direction = self.turning_policy(self.car_simulation)
        best_speed_modification = self.find_best_speed_modification()

        self.car_simulation.turn(best_turn_direction)
        self.car_simulation.apply_speed_modification(best_speed_modification)
        self.car_simulation.move()

        self.car.turn(best_turn_direction)
        self.car.apply_speed_modification(best_speed_modification)
        self.car.move()
