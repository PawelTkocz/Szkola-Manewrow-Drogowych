import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree

from Geometry import Directions, Rectangle
from autonomousDriving.CarSimulation import CarSimulation
from cars.Car import Car


class BasicAutonomousDriving:

    def __init__(self, car: Car, curve_points):
        self.car = car
        self.curve_points = curve_points
        self.tree = KDTree(self.curve_points)
        self.car_simulation = CarSimulation(
            car.brand, car.front_left, car.direction, car.velocity
        )

    def simulate_move(self):

        turn_options = [Directions.LEFT, Directions.FRONT, Directions.RIGHT]

        results = []
        for turn_option in turn_options:
            start_state = self.car_simulation.get_state()
            self.car_simulation.turn(turn_option)
            self.car_simulation.move()
            results.append(self.evaluate_situation(self.car_simulation))
            self.car_simulation.set_state(start_state)

        self.car.turn(turn_options[results.index(min(results))])
        self.car.speed_up(Directions.FRONT)
        self.car.move()
        self.car_simulation.turn(turn_options[results.index(min(results))])
        self.car_simulation.speed_up(Directions.FRONT)
        self.car_simulation.move()
        print(turn_options[results.index(min(results))])

    def evaluate_situation(self, car: Car):
        distance, index = self.tree.query([car.front_left.x, car.front_left.y])
        return distance
