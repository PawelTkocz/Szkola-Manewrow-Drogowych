from car.instruction_controlled_car import SpeedInstruction
from car.model import CarModel
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track import (
    ManoeuvreTrack,
)
from smart_city.road_control_center.preprocessed_manoeuvres.manoeuvre_preprocessing_manager.manoeuvre_tracks.manoeuvre_track_segments.manoeuvre_track_segment import (
    TrackSegmentType,
)
from smart_city.road_control_center.utils import (
    get_turn_instruction,
)
from smart_city.road_control_center.car_simulation import CarSimulation


class TrackVelocitiesCalculator:
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

        while not car_simulation.is_point_inside(manoeuvre_track.end_point):
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
                    else car_simulation.max_velocity
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
                    "speed_instruction": speed_instruction,
                    "turn_instruction": get_turn_instruction(
                        manoeuvre_track,
                        car_simulation.get_live_data(),
                        speed_instruction,
                    ),
                }
            )
        return False

    def get_max_safe_velocities(
        self, manoeuvre_track: ManoeuvreTrack, car_model: CarModel
    ) -> list[float]:
        max_safe_velocities: list[float] = [8]
        # start_max_safe_velocity = self.get_start_max_safe_velocity(
        #     manoeuvre_track, car_model
        # )
        return max_safe_velocities * len(manoeuvre_track.track_path)
