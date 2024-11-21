import math
from autonomousDriving.Track import Track
from cars.BasicBrand import BasicBrand
from cars.Car import Car


class CarSimulation2(Car):
    """
    Class simulating movement of the car on track
    """

    def __init__(self, car: Car, track: list[tuple[float, float]]):
        """
        Initialize car simulation
        """
        super().__init__(
            BasicBrand("blue"), car.front_middle, car.direction, car.velocity
        )
        self.track = Track(track, 5)

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

    def will_go_off_track(
        self,
        max_distance_to_track: float,
        max_steps_into_future: int,
        turning_policy,
        speed_modification_policy,  # maybe add in the future
    ):
        """
        Check if car will go off track
        """
        if self.find_distance_to_track() > max_distance_to_track:
            return True
        start_state = self.get_state()
        went_off_track = False
        for _ in range(max_steps_into_future):
            turn_direction = turning_policy(self)  # better pass state instead of self
            self.turn(turn_direction)
            self.move()
            if self.find_distance_to_track() > max_distance_to_track:
                went_off_track = True
                break
            if self.velocity == 0:
                break
        self.set_state(start_state)
        return went_off_track

    def find_distance_to_point(self, point: tuple[float, float]):
        x1, y1 = point[0], point[1]
        x2, y2 = self.front_middle.x, self.front_middle.y
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def find_distance_to_track(self):
        return self.track.find_distance_to_point(self.front_middle)

    def find_index_of_closest_point_on_track(self):
        return self.track.find_index_of_closest_point(self.front_middle)

    def find_straight_line_end_point_on_track(self, point_index):
        return self.track.find_straight_line_end_point(point_index)
