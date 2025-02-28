from car.car import Car, CarState, SpeedModifications
from car.autonomous.car_simulation import CarSimulation
from car.autonomous.track import Track, TrackPath
from car.autonomous.track_follower import MovementDecision, TrackFollower
from car.model import CarModel
from geometry import Directions


class TrackFollowerAlpha(TrackFollower):
    def __init__(self, model: CarModel):
        self.car_simulation = CarSimulation(model)
        self.max_distance_to_track = 5

    def set_track(self, track_path: TrackPath) -> None:
        self.track = Track(track_path)

    def make_movement_decision(self, car_state: CarState) -> MovementDecision:
        return {"speed_modification": None, "turn_direction": None}

    def closest_to_track_turning_policy(self, car_state: CarState):
        min_distance = None
        best_turn_direction = None

        # self.car_simulation.set_state()
        for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
            car_simulation = self.car_simulation
            start_state = car_simulation.get_current_state()
            car_simulation.turn(turn_direction)
            car_simulation.move()
            distance = self.distance_to_track(car_simulation)
            if min_distance is None or distance < min_distance:
                best_turn_direction = turn_direction
                min_distance = distance
            car_simulation.set_state(start_state)

        return best_turn_direction
    
    def hold_to_track(
        self,
    ):
        car_simulation = self.car_simulation
        for speed_modification in [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]:
            start_state = car_simulation.get_state()
            car_simulation.apply_speed_modification(speed_modification)
            car_simulation.move()
            will_go_off_track = self.will_go_off_track()
            car_simulation.set_state(start_state)
            if not will_go_off_track:
                return speed_modification
        return SpeedModifications.BRAKE
    
    def will_go_off_track(self):
        """
        Check if car will go off track.
        """
        if self.distance_to_track(self.car_simulation) > self.max_distance_to_track:
            return True
        start_state = self.car_simulation.get_state()
        went_off_track = False
        for _ in range(self.max_steps_into_future):
            turn_direction = self.hold_to_track()
            self.car_simulation.turn(turn_direction)
            self.car_simulation.move()
            if self.distance_to_track(self.car_simulation) > self.max_distance_to_track:
                went_off_track = True
                break
            if self.car_simulation.velocity == 0:
                break
        self.car_simulation.set_state(start_state)
        return went_off_track
    
    def distance_to_track(self, car: Car):
        return self.track.get_distance_to_point(car.front_middle)