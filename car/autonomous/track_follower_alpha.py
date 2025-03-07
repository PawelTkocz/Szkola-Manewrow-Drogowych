from car.car import Car, LiveCarData, SpeedModifications
from car.autonomous.car_simulation import CarSimulation
from car.autonomous.track import Track, TrackPath
from car.autonomous.track_follower import MovementDecision, TrackFollower
from geometry import Directions
from manoeuvres.manoeuvre_phase import ManoeuvrePhaseEndState


class TrackFollowerAlpha(TrackFollower):
    def __init__(self):
        self.max_distance_to_track = 5
        self.simulation_max_future_steps = 5

    def set_track(self, track_path: TrackPath) -> None:
        self.track = Track(track_path)

    def make_movement_decision(self, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState) -> MovementDecision:
        turn_direction = self.closest_to_track_turning_policy(live_car_data, desired_end_state)
        speed_modification = self.hold_to_track(live_car_data, desired_end_state)
        return {"speed_modification": speed_modification, "turn_direction": turn_direction}

    def closest_to_track_turning_policy(self, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState) -> Directions:
        min_distance = None
        best_turn_direction = None

        car_simulation = CarSimulation(live_car_data)
        for turn_direction in [Directions.FRONT, Directions.LEFT, Directions.RIGHT]:
            start_state = car_simulation.get_current_state()
            car_simulation.move(movement_decision={"turn_direction": turn_direction, "speed_modification": SpeedModifications.NO_CHANGE})
            distance = self.distance_to_track(car_simulation)
            if min_distance is None or distance < min_distance:
                best_turn_direction = turn_direction
                min_distance = distance
            car_simulation.restore_state(start_state)

        return best_turn_direction
    
    def hold_to_track(
        self, live_car_data: LiveCarData, desired_end_state: ManoeuvrePhaseEndState
    ):
        car_simulation = CarSimulation(live_car_data)
        for speed_modification in [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]:
            start_state = car_simulation.get_current_state()
            turn_direction = self.closest_to_track_turning_policy(live_car_data, desired_end_state)
            car_simulation.move(movement_decision={"turn_direction": turn_direction, "speed_modification": speed_modification})
            will_go_off_track = self.will_go_off_track(car_simulation)
            meets_end_state_condition = self.meets_end_state_condition(car_simulation, desired_end_state)
            car_simulation.restore_state(start_state)
            if not will_go_off_track and meets_end_state_condition:
                return speed_modification
        return SpeedModifications.BRAKE
    
    def meets_end_state_condition(self, car_simulation: CarSimulation, end_state: ManoeuvrePhaseEndState) -> bool:
        closest_track_point_index = self.index_of_closest_track_point(car_simulation)
        goal_point_track_index = self.track.find_index_of_closest_point(end_state["front_middle_position"])
        start_state = car_simulation.get_current_state()
        result = False
        while closest_track_point_index <= goal_point_track_index:
            if car_simulation.velocity <= end_state["velocity"]:
                result = True
                break
            car_simulation.move(movement_decision={"turn_direction": self.hold_to_track(car_simulation.get_live_data()), "speed_modification": SpeedModifications.BRAKE})
            closest_track_point_index = self.index_of_closest_track_point(car_simulation)
        car_simulation.restore_state(start_state)
        return result

    def will_go_off_track(self, car_simulation: CarSimulation):
        """
        Check if car will go off track.
        """
        if self.distance_to_track(car_simulation) > self.max_distance_to_track:
            return True
        start_state = car_simulation.get_current_state()
        went_off_track = False
        for _ in range(self.simulation_max_future_steps):
            car_simulation.move(movement_decision={"turn_direction": self.hold_to_track(car_simulation.get_live_data()), "speed_modification": SpeedModifications.NO_CHANGE})
            if self.distance_to_track(car_simulation) > self.max_distance_to_track:
                went_off_track = True
                break
            if car_simulation.velocity == 0:
                break
        car_simulation.restore_state(start_state)
        return went_off_track
    
    def distance_to_track(self, car: Car):
        return self.track.get_distance_to_point(car.front_middle)
    
    def index_of_closest_track_point(self, car: Car):
        return self.track.find_index_of_closest_point(car.front_middle)