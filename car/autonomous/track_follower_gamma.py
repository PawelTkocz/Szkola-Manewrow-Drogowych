from car.autonomous.car_simulation import CarSimulation
from car.autonomous.track import TrackPath
from car.autonomous.track_follower import MovementDecision, TrackFollower
from car.car import CarState
from car.model import CarModel
from geometry import Directions


class TrackFollowerGamma(TrackFollower):
    def __init__(self, model: CarModel):
        self.car_simulation = CarSimulation(model)

    def set_track(self, track_path: TrackPath) -> None:
        self.track_path = track_path

    def make_movement_decision(self, car_state: CarState) -> MovementDecision:

        return {"speed_modification": None, "turn_direction": None}

    def dont_speed_up_if_will_go_off_track(
        car_simulation: CarSimulation,
        max_distance_to_track,
        max_steps_into_future,
        turning_policy,
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
                max_steps_into_future,
                turning_policy,
            )
            car_simulation.set_state(start_state)
            if not will_go_off_track:
                return speed_modification
        return SpeedModifications.BRAKE

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
