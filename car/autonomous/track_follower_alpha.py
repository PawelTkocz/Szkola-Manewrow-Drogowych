from car.autonomous.car_simulation import CarSimulation
from car.autonomous.track import TrackPath
from car.autonomous.track_follower import MovementDecision, TrackFollower
from car.car_state import CarState
from car.model import CarModel
from geometry import Directions


class TrackFollowerAlpha(TrackFollower):
    def __init__(self, model: CarModel):
        self.car_simulation = CarSimulation(model)

    def set_track(self, track_path: TrackPath) -> None:
        self.track_path = track_path

    def make_movement_decision(self, car_state: CarState) -> MovementDecision:

        return {"speed_modification": None, "turn_direction": None}

    def closest_to_track_turning_policy(self, car_state: CarState):
        min_distance = None
        best_turn_direction = None

        for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
            car_simulation = self.car_simulation
            start_state = car_simulation.get_state()
            car_simulation.turn(turn_direction)
            car_simulation.move()
            distance = car_simulation.find_distance_to_track()
            if min_distance is None or distance < min_distance:
                best_turn_direction = turn_direction
                min_distance = distance
            car_simulation.set_state(start_state)

        return best_turn_direction
    
    def hold_to_track_with_preference(
        car_simulation: CarSimulation,
        max_distance_to_track,
        max_steps_into_future,
        turning_policy,
        simulation_speed_policy,
        non_preference_zone,
        cars: list["CarSimulation"],
    ):
        for speed_modification in [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]:
            start_state = car_simulation.get_state()
            car_simulation.apply_speed_modification(speed_modification)
            car_simulation.move()
            will_go_off_track = car_simulation.will_go_off_track(
                max_distance_to_track,
                1,
                turning_policy,
            )
            will_collide = car_simulation.will_collide(
                max_steps_into_future,
                turning_policy,
                non_preference_zone,
            )
            car_simulation.set_state(start_state)
            if not will_go_off_track and not will_collide:
                return speed_modification
            if will_go_off_track:
                continue
            # will collide
            # check if you can escape non preference zone without collisions
            # return SpeedModifications.BRAKE
            # return SpeedModifications.NO_CHANGE
            # to juz jest po set_state(start_state) wiec dla wszystkich speed mod wynik ten sam
            if len(cars) == 0 or not car_simulation.will_violate_the_right_of_way(
                turning_policy, simulation_speed_policy, non_preference_zone, cars
            ):
                return speed_modification
        return SpeedModifications.BRAKE

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


    def find_distance_to_track(self):
        return self.track.find_distance_to_point(self.front_middle)