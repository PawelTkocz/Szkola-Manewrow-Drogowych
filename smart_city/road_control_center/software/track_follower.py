from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
)
from geometry import Point
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.software.car_simulation import CarSimulation
from smart_city.schemas import LiveCarData


class TrackFollower:
    def __init__(self):
        self.max_distance_to_track = 5
        self.simulation_max_future_steps = 5

    def get_turn_instruction(
        self,
        live_car_data: LiveCarData,
        track: Track,
        speed_instruction: SpeedInstruction,
    ) -> TurnInstruction:
        def _distance_to_track_after_instruction(
            turn_instruction: TurnInstruction,
        ) -> float:
            car_simulation = CarSimulation(live_car_data)
            car_simulation.move(
                {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": turn_instruction,
                }
            )
            return self.distance_to_track(car_simulation.get_live_data(), track)

        return min(TurnInstruction, key=_distance_to_track_after_instruction)

    def get_valid_speed_instructions(self, velocity: float) -> list[SpeedInstruction]:
        if velocity == 0:
            return list(SpeedInstruction)
        if velocity > 0:
            return [
                SpeedInstruction.ACCELERATE_FRONT,
                SpeedInstruction.NO_CHANGE,
                SpeedInstruction.BRAKE,
            ]
        return [
            SpeedInstruction.ACCELERATE_REVERSE,
            SpeedInstruction.NO_CHANGE,
            SpeedInstruction.BRAKE,
        ]

    def get_car_control_instructions(
        self,
        live_car_data: LiveCarData,
        track: Track,
        stop_point: Point | None = None,
    ) -> CarControlInstructions:
        speed_instructions = self.get_valid_speed_instructions(
            live_car_data["live_state"]["velocity"]
        )
        for speed_instruction in speed_instructions[:-1]:
            if self.is_speed_instruction_safe(
                live_car_data, track, stop_point, speed_instruction
            ):
                turn_instruction = self.get_turn_instruction(
                    live_car_data, track, speed_instruction
                )
                return {
                    "turn_instruction": turn_instruction,
                    "speed_instruction": speed_instruction,
                }
        return {
            "speed_instruction": speed_instructions[-1],
            "turn_instruction": self.get_turn_instruction(
                live_car_data, track, speed_instruction
            ),
        }

    def is_speed_instruction_safe(
        self,
        live_car_data: LiveCarData,
        track: Track,
        stop_point: Point | None,
        speed_instruction: SpeedInstruction,
    ) -> bool:
        car_simulation = CarSimulation(live_car_data)
        turn_instruction = self.get_turn_instruction(
            live_car_data, track, speed_instruction
        )
        car_control_instructions: CarControlInstructions = {
            "turn_instruction": turn_instruction,
            "speed_instruction": speed_instruction,
        }
        car_simulation.move(car_control_instructions)
        will_go_off_track = self.will_go_off_track(car_simulation, track)
        if will_go_off_track:
            return False
        if not stop_point or self.can_stop_at_stop_point(
            car_simulation, track, stop_point
        ):
            return True
        return False

    def can_stop_at_stop_point(
        self,
        car_simulation: CarSimulation,
        track: Track,
        stop_point: Point,
    ) -> bool:
        closest_track_point_index = self.index_of_closest_track_point(
            car_simulation, track
        )
        stop_point_track_index = track.find_index_of_closest_point(stop_point)
        while closest_track_point_index <= stop_point_track_index:
            if car_simulation.velocity == 0:
                return True
            car_simulation.move(
                {
                    "speed_instruction": SpeedInstruction.BRAKE,
                    "turn_instruction": self.get_turn_instruction(
                        car_simulation.get_live_data(), track, SpeedInstruction.BRAKE
                    ),
                }
            )
            closest_track_point_index = self.index_of_closest_track_point(
                car_simulation, track
            )
        return False

    def will_go_off_track(
        self,
        car_simulation: CarSimulation,
        track: Track,
    ):
        """
        Check if car will go off track.
        """
        if self.distance_to_track(car_simulation, track) > self.max_distance_to_track:
            return True
        for _ in range(self.simulation_max_future_steps):
            car_simulation.move(
                {
                    "speed_instruction": SpeedInstruction.BRAKE,
                    "turn_instruction": self.get_turn_instruction(
                        car_simulation.get_live_data(), track, SpeedInstruction.BRAKE
                    ),
                }
            )  # was no change before
            if (
                self.distance_to_track(car_simulation, track)
                > self.max_distance_to_track
            ):
                return True
            if car_simulation.velocity == 0:
                return False
        return False

    def distance_to_track(self, car_simulation: CarSimulation, track: Track):
        return track.get_distance_to_point(car_simulation.front_middle)

    def index_of_closest_track_point(self, car_simulation: CarSimulation, track: Track):
        return track.find_index_of_closest_point(car_simulation.front_middle)
