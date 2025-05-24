from typing import Callable
from car.instruction_controlled_car import SpeedInstruction
from car.model import CarModelSpecification
from geometry.vector import Point
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track import (
    ManoeuvreTrack,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.manoeuvre_tracks.manoeuvre_track_segment import (
    ManoeuvreTrackSegment,
    TrackSegmentType,
)
from traffic_control_system.road_control_center.manoeuvres_preprocessing.schemas import (
    ManoeuvreStartCarState,
)
from traffic_control_system.road_control_center.utils import (
    get_turn_instruction,
)
from traffic_control_system.road_control_center.car_simulation import CarSimulation

MAX_DISTANCE_TO_TRACK = 3
MIN_VELOCITY = 1
MAX_SAFE_VELOCITY_ACCURACY = 0.5
VELOCITY_SAFE_MARGIN = 0.8


class TrackVelocitiesPreprocessor:
    def __init__(
        self,
        manoeuvre_track: ManoeuvreTrack,
        car_model_specification: CarModelSpecification,
    ) -> None:
        self.manoeuvre_track = manoeuvre_track
        self.car_model_specification = car_model_specification
        self.first_track_point_index = self._get_first_track_point_index()
        self.car_start_states = self._get_car_start_states()
        self.track_segments_max_const_velocities: dict[ManoeuvreTrackSegment, float] = (
            self._get_track_segments_max_const_velocities()
        )

    def _get_first_track_point_index(self) -> int:
        start_state = self.manoeuvre_track.start_car_state
        car_simulation = CarSimulation(
            start_state["front_middle"],
            start_state["direction"],
            start_state["wheels_angle"],
            MIN_VELOCITY,
            self.car_model_specification,
        )
        return self.manoeuvre_track.find_index_of_closest_point(
            car_simulation.axle_center
        )

    def _get_car_start_states(
        self,
    ) -> dict[int, ManoeuvreStartCarState]:
        start_states: dict[int, ManoeuvreStartCarState] = {}
        start_state = self.manoeuvre_track.start_car_state
        start_states[self.first_track_point_index] = start_state
        car_simulation = CarSimulation(
            start_state["front_middle"],
            start_state["direction"],
            start_state["wheels_angle"],
            MIN_VELOCITY,
            self.car_model_specification,
        )

        while not car_simulation.is_point_inside(self.manoeuvre_track.end_point):
            if (
                self.manoeuvre_track.get_distance_to_point(car_simulation.axle_center)
                > MAX_DISTANCE_TO_TRACK
            ):
                raise ValueError("Not possible to complete the track")

            track_point_index = self.manoeuvre_track.find_index_of_closest_point(
                car_simulation.axle_center
            )
            start_states[track_point_index] = {
                "direction": car_simulation.direction,
                "front_middle": car_simulation.front_middle,
                "wheels_angle": car_simulation.wheels_angle,
            }

            speed_instruction: SpeedInstruction = SpeedInstruction.NO_CHANGE
            car_simulation.move(
                {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": get_turn_instruction(
                        self.manoeuvre_track,
                        car_simulation.get_live_data(),
                        speed_instruction,
                    ),
                }
            )
            car_simulation.set_velocity(MIN_VELOCITY)

        for index in range(
            self.first_track_point_index + 1, len(self.manoeuvre_track.track_path)
        ):
            if index not in start_states:
                start_states[index] = start_states[index - 1]
        return start_states

    def get_max_safe_velocity(
        self,
        start_point_index: int,
        end_point_index: int,
        car_simulation_controller: Callable[[CarSimulation, ManoeuvreTrack], None],
        velocity_safe_margin: float,
    ) -> float:
        max_velocity = self.car_model_specification["motion"]["max_velocity"]
        start_car_state = self.car_start_states[start_point_index]
        car_simulation = CarSimulation(
            start_car_state["front_middle"],
            start_car_state["direction"],
            start_car_state["wheels_angle"],
            max_velocity,
            self.car_model_specification,
        )
        if not self.will_go_off_track(
            car_simulation, car_simulation_controller, end_point_index
        ):
            return max_velocity * velocity_safe_margin

        min_velocity: float = MIN_VELOCITY
        while max_velocity - min_velocity > MAX_SAFE_VELOCITY_ACCURACY:
            v = (max_velocity + min_velocity) / 2
            car_simulation = CarSimulation(
                start_car_state["front_middle"],
                start_car_state["direction"],
                start_car_state["wheels_angle"],
                v,
                self.car_model_specification,
            )
            if not self.will_go_off_track(
                car_simulation, car_simulation_controller, end_point_index
            ):
                min_velocity = v
            else:
                max_velocity = v
        return min_velocity * velocity_safe_margin

    def _get_track_segments_max_const_velocities(
        self,
    ) -> dict[ManoeuvreTrackSegment, float]:
        def _car_simulation_controller(
            _car_simulation: CarSimulation, _manoeuvre_track: ManoeuvreTrack
        ) -> None:
            current_speed = _car_simulation.velocity
            speed_instruction: SpeedInstruction = SpeedInstruction.NO_CHANGE
            _car_simulation.move(
                {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": get_turn_instruction(
                        _manoeuvre_track,
                        _car_simulation.get_live_data(),
                        speed_instruction,
                    ),
                }
            )
            _car_simulation.set_velocity(current_speed)

        cur_segment_start_index = self.first_track_point_index
        result: dict[ManoeuvreTrackSegment, float] = {}
        for track_segment_data in self.manoeuvre_track.segments_data:
            track_segment = track_segment_data["track_segment"]
            segment_cumulative_length = track_segment_data["cumulative_track_length"]
            result[track_segment] = self.get_max_safe_velocity(
                cur_segment_start_index,
                segment_cumulative_length - 1,
                _car_simulation_controller,
                VELOCITY_SAFE_MARGIN,
            )
            cur_segment_start_index = segment_cumulative_length
        return result

    def will_go_off_track(
        self,
        car_simulation: CarSimulation,
        car_simulation_controller: Callable[[CarSimulation, ManoeuvreTrack], None],
        end_point_index: int,
    ) -> bool:
        manoeuvre_track = self.manoeuvre_track
        end_point = Point(*manoeuvre_track.track_path[end_point_index])
        while not car_simulation.is_point_inside(end_point):
            distance_to_track = manoeuvre_track.get_distance_to_point(
                car_simulation.axle_center
            )
            if distance_to_track > MAX_DISTANCE_TO_TRACK:
                return True
            car_simulation_controller(car_simulation, manoeuvre_track)
        return False

    def get_max_safe_velocities(
        self,
    ) -> list[float]:
        def _car_simulation_controller(
            _car_simulation: CarSimulation, _manoeuvre_track: ManoeuvreTrack
        ) -> None:
            track_point_index = _manoeuvre_track.find_index_of_closest_point(
                _car_simulation.axle_center
            )
            incoming_segments_data = _manoeuvre_track.get_incoming_segments_data(
                track_point_index
            )
            current_track_segment = incoming_segments_data["current_track_segment"]
            next_track_segment = incoming_segments_data["next_track_segment"]
            min_velocity = (
                self.track_segments_max_const_velocities[next_track_segment]
                if current_track_segment.type == TrackSegmentType.STRAIGHT_PATH
                and next_track_segment
                else self.track_segments_max_const_velocities[current_track_segment]
            )
            speed_instruction: SpeedInstruction = SpeedInstruction.NO_CHANGE
            if _car_simulation.velocity > min_velocity:
                speed_instruction = SpeedInstruction.BRAKE
            elif _car_simulation.velocity + _car_simulation.acceleration < min_velocity:
                speed_instruction = SpeedInstruction.ACCELERATE_FORWARD
            _car_simulation.move(
                {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": get_turn_instruction(
                        _manoeuvre_track,
                        _car_simulation.get_live_data(),
                        speed_instruction,
                    ),
                }
            )

        track_len = len(self.manoeuvre_track.track_path)
        max_safe_velocities = []
        for i in range(track_len):
            if i < self.first_track_point_index:
                max_safe_velocities.append(
                    self.car_model_specification["motion"]["max_velocity"]
                )
                continue
            max_safe_velocities.append(
                self.get_max_safe_velocity(
                    i, track_len - 1, _car_simulation_controller, VELOCITY_SAFE_MARGIN
                )
            )
        return max_safe_velocities
