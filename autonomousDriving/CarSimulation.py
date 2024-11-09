from Geometry import Directions
from cars.Car import Car


class CarSimulation(Car):

    def set_state(self, state: dict):
        self.velocity = state["velocity"]
        self.wheels.direction = state["wheels"]
        self.body._direction = state["body"]["direction"]
        self.body._front_left = state["body"]["front_left"]
        self.body._front_right = state["body"]["front_right"]
        self.body._rear_left = state["body"]["rear_left"]
        self.body._rear_right = state["body"]["rear_right"]

    def get_state(self):
        return {
            "velocity": self.velocity,
            "body": {
                "direction": self.direction,
                "front_left": self.front_left,
                "front_right": self.front_right,
                "rear_left": self.rear_left,
                "rear_right": self.rear_right,
            },
            "wheels": self.wheels.direction,
        }
