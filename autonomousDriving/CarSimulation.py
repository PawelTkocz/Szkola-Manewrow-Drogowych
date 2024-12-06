import math
from Geometry import Rectangle
from autonomousDriving.Track import Track
from cars.Car import Car


class CarSimulation(Car):
    """
    Class simulating movement of the car on track
    """

    def __init__(self, car: Car, track: list[tuple[float, float]]):
        """
        Initialize car simulation
        """
        super().__init__(car.brand, car.front_middle, car.direction, car.velocity)
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

    def will_go_off_track(
        self,
        max_distance_to_track: float,
        max_steps_into_future: int,
        turning_policy,
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

    def will_collide(self, max_steps_into_future: int, turning_policy, obj: Rectangle):
        if self.collides(obj):
            return True
        start_state = self.get_state()
        collides = False
        for _ in range(max_steps_into_future):
            turn_direction = turning_policy(self)  # better pass state instead of self
            self.turn(turn_direction)
            self.brake()
            self.move()
            if self.collides(obj):
                collides = True
                break
            if self.velocity == 0:
                break
        self.set_state(start_state)
        return collides

    def will_violate_the_right_of_way(
        self,
        turning_policy,
        speed_policy,
        non_preference_zone: Rectangle,
        cars: list["CarSimulation"],
    ):
        if self.body.collides(non_preference_zone) and any(
            car.body.collides(non_preference_zone) for car in cars
        ):
            return True
        self_start_state = self.get_state()
        cars_state = [car.get_state() for car in cars]
        collides = False
        cnt = 0
        entered_non_preference_zone = False
        while True:  # trzeba naprawic
            cnt += 1
            turn_direction = turning_policy(self)  # better pass state instead of self
            speed_modification = speed_policy(self)
            self.turn(turn_direction)
            self.apply_speed_modification(speed_modification)
            self.move()

            for car in cars:
                turn_direction = turning_policy(
                    car
                )  # better pass state instead of self
                speed_modification = speed_policy(car)
                car.turn(turn_direction)
                car.apply_speed_modification(speed_modification)
                car.move()

            if self.body.collides(non_preference_zone) and any(
                car.body.collides(non_preference_zone) for car in cars
            ):
                collides = True
                break
            if self.body.collides(non_preference_zone):
                entered_non_preference_zone = True
            elif entered_non_preference_zone:
                break
        self.set_state(self_start_state)
        for index, car in enumerate(cars):
            car.set_state(cars_state[index])
        return collides

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
