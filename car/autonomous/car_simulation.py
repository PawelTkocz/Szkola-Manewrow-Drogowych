from car.car import Car
from car.car_state import CarState
from car.model import CarModel
from geometry import Direction, Point


class CarSimulation(Car):
    """
    Class simulating real car.
    """

    def __init__(self, model: CarModel):
        """
        Initialize car simulation
        """
        super().__init__(model, "black", Point(0, 0), Direction(Point(1, 0)))

    def set_state(self, car_state: CarState):
        self.velocity = car_state.velocity
        # self.wheels.direction = state["wheels"].copy()
        self.body._direction = car_state.direction.copy()
        self.body._front_middle = car_state.front_middle.copy()
        self.body._rear_middle = car_state.rear_middle.copy()
        self.body._front_left = car_state.front_left.copy()
        self.body._front_right = car_state.front_right.copy()
        self.body._rear_left = car_state.rear_left.copy()
        self.body._rear_right = car_state.rear_right.copy()
