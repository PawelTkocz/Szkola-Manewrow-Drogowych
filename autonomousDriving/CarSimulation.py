from Geometry import Directions
from cars.Car import Car


class CarSimulation(Car):

    def set_state(self, state: dict):
        self.velocity = state["velocity"]
        self.wheels.direction = state["wheels"].copy()
        self.body._direction = state["body"]["direction"].copy()
        self.body._front_middle = state["body"]["front_middle"].copy()
        self.body._front_left = state["body"]["front_left"].copy()
        self.body._front_right = state["body"]["front_right"].copy()
        self.body._rear_left = state["body"]["rear_left"].copy()
        self.body._rear_right = state["body"]["rear_right"].copy()

    def get_state(self):
        return {
            "velocity": self.velocity,
            "body": {
                "direction": self.direction,
                "front_middle": self.front_middle,
                "front_left": self.front_left,
                "front_right": self.front_right,
                "rear_left": self.rear_left,
                "rear_right": self.rear_right,
            },
            "wheels": self.wheels.direction.copy(),
        }
