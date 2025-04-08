from abc import ABC, abstractmethod

from car.instruction_controlled_car import SpeedInstruction, TurnSignalsInstruction
from car.model import CarModel
from geometry import Point
from smart_city.road_control_center.manoeuvres.schemas import TrackPointData, TurnSignal
from smart_city.road_control_center.manoeuvres.track_preprocessor.manoeuvre_track import (
    ManoeuvreTrack,
)
from smart_city.road_control_center.manoeuvres.track_preprocessor.manoeuvre_track_segment import (
    TrackSegmentType,
)
from smart_city.road_control_center.software.car_simulation import CarSimulation


class ManoeuvreTrackPreprocessor(ABC):
    def preprocess_track(
        self, manoeuvre_track: ManoeuvreTrack, car_model: CarModel
    ) -> list[TrackPointData]:
        max_safe_velocities = self.get_max_safe_velocities(manoeuvre_track, car_model)
        preprocessed_track_points: list[TrackPointData] = []
        for point_index, track_point in enumerate(manoeuvre_track.track_path):
            preprocessed_track_points.append(
                {
                    "point": Point(track_point[0], track_point[1]),
                    "max_safe_velocity": max_safe_velocities[point_index],
                    "turn_signal": self.get_track_point_turn_signal(
                        point_index, manoeuvre_track
                    ),
                }
            )
        return preprocessed_track_points

    @abstractmethod
    def get_track_point_turn_signal(
        self, track_point_index: int, manoeuvre_track: ManoeuvreTrack
    ) -> TurnSignal:
        raise NotImplementedError

    def get_start_max_safe_velocity(
        self, manoeuvre_track: ManoeuvreTrack, car_model: CarModel
    ) -> float:
        start_car_state = manoeuvre_track.start_car_state
        max_velocity = car_model.max_velocity
        car_simulation = CarSimulation(
            start_car_state["front_middle"],
            start_car_state["direction"],
            start_car_state["wheels_direction"],
            max_velocity,
            car_model,
        )
        if not self.will_go_off_track(car_simulation, manoeuvre_track):
            return max_velocity

        min_velocity = car_model.max_acceleration
        while max_velocity - min_velocity > 0.5:
            v = (max_velocity - min_velocity) / 2
            car_simulation = CarSimulation(
                start_car_state["front_middle"],
                start_car_state["direction"],
                start_car_state["wheels_direction"],
                v,
                car_model,
            )
            if not self.will_go_off_track(car_simulation, manoeuvre_track):
                min_velocity = v
            else:
                max_velocity = v
        return min_velocity

    def will_go_off_track(
        self,
        car_simulation: CarSimulation,
        manoeuvre_track: ManoeuvreTrack,
    ) -> bool:
        """
        Check if car will go off track.
        """
        # min velocity mozna wyznaczyc wyznaczajac max const velocity na calym odcinku
        max_distance_to_track = 3

        while not car_simulation.car.is_point_inside(manoeuvre_track.end_point):
            track_point_index = manoeuvre_track.find_index_of_closest_point(
                car_simulation.front_middle
            )
            distance_to_track = manoeuvre_track.get_distance_to_point(
                car_simulation.front_middle
            )
            if distance_to_track > max_distance_to_track:
                return True
            incoming_segments_data = manoeuvre_track.get_incoming_segments_data(
                track_point_index
            )
            current_track_segment = incoming_segments_data["current_track_segment"]
            next_track_segment = incoming_segments_data["next_track_segment"]
            min_velocity = current_track_segment.expected_min_velocity
            if current_track_segment.type == TrackSegmentType.STRAIGHT_PATH:
                min_velocity = (
                    next_track_segment.expected_min_velocity
                    if next_track_segment
                    else car_simulation.car.model.max_velocity
                )
            if min_velocity is None:
                print("No minimum velocity set error")
                return True

            speed_instruction: SpeedInstruction = SpeedInstruction.NO_CHANGE
            if car_simulation.velocity > min_velocity:
                speed_instruction = SpeedInstruction.BRAKE
            elif car_simulation.velocity < min_velocity:
                speed_instruction = SpeedInstruction.ACCELERATE_FRONT
            car_simulation.move(
                {
                    "movement_instructions": {
                        "speed_instruction": speed_instruction,
                        "turn_instruction": car_simulation.get_turn_instruction(
                            manoeuvre_track, speed_instruction
                        ),
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
                }
            )
        return False

    def get_max_safe_velocities(
        self, manoeuvre_track: ManoeuvreTrack, car_model: CarModel
    ) -> list[float]:
        max_safe_velocities: list[float] = []
        start_max_safe_velocity = self.get_start_max_safe_velocity(
            manoeuvre_track, car_model
        )
        return [start_max_safe_velocity] * len(manoeuvre_track.track_path)
