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
