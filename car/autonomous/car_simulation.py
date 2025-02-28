from typing import TypedDict
from car.car import Car, LiveCarData
from car.model import CarModel
from geometry import Direction, Point


class CarSavedState(TypedDict):
    velocity: float
    direction: Direction
    front_left: Point
    front_middle: Point
    front_right: Point
    rear_left: Point
    rear_middle: Point
    rear_right: Point
    wheels_direction: Direction
    model: CarModel


class CarSimulation(Car):
    """
    Class simulating real car.
    """

    def __init__(self, model: CarModel, live_car_data: LiveCarData):
        """
        Initialize car simulation.
        """
        super().__init__(
            model,
            live_car_data.color,
            live_car_data.front_middle,
            live_car_data.direction,
            live_car_data.velocity,
        )

    def set_state(self, car_saved_state: CarSavedState):
        # make sure it's not necessary to create copies here
        self._direction = car_saved_state["direction"]
        self._front_left = car_saved_state["front_left"]
        self._front_middle = car_saved_state["front_middle"]
        self._front_right = car_saved_state["front_right"]
        self._rear_left = car_saved_state["rear_left"]
        self._rear_middle = car_saved_state["rear_middle"]
        self._rear_right = car_saved_state["rear_right"]
        self.velocity = car_saved_state["velocity"]
        self.wheels._direction = car_saved_state["wheels_direction"]
        self.model = car_saved_state["model"]

    def get_current_state(self) -> CarSavedState:
        return {
            "direction": self.direction,
            "front_left": self.front_left,
            "front_middle": self.front_middle,
            "front_right": self.front_right,
            "rear_left": self.rear_left,
            "rear_middle": self.rear_middle,
            "rear_right": self.rear_right,
            "velocity": self.velocity,
            "wheels_direction": self.wheels_direction,
            "model": self.model,
        }
