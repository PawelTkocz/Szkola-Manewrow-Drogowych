from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)
from geometry import Point
from smart_city.road_control_center.manoeuvres.manoeuvre_track import ManoeuvreTrack
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.software.car_simulation import CarSimulation
from smart_city.schemas import LiveCarData


class TrackFollower:
    def __init__(self) -> None:
        self.max_distance_to_track = 3
        self.simulation_max_future_steps = 100

    def get_turn_instruction(
        self,
        live_car_data: LiveCarData,
        track: Track,
        speed_instruction: SpeedInstruction,
    ) -> TurnInstruction:
        def _distance_to_track_after_instruction(
            turn_instruction: TurnInstruction,
        ) -> float:
            car_simulation = CarSimulation.from_live_car_data(live_car_data)
            car_simulation.move(
                {
                    "movement_instructions": {
                        "speed_instruction": speed_instruction,
                        "turn_instruction": turn_instruction,
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
                }
            )
            return self.distance_to_track(car_simulation, track)

        if live_car_data["live_state"]["velocity"] == 0:
            return TurnInstruction.NO_CHANGE
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
                    "movement_instructions": {
                        "turn_instruction": turn_instruction,
                        "speed_instruction": speed_instruction,
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
                }
        return {
            "movement_instructions": {
                "speed_instruction": speed_instructions[-1],
                "turn_instruction": self.get_turn_instruction(
                    live_car_data, track, speed_instruction
                ),
            },
            "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
        }

    def is_speed_instruction_safe(
        self,
        live_car_data: LiveCarData,
        track: Track,
        stop_point: Point | None,
        speed_instruction: SpeedInstruction,
    ) -> bool:
        car_simulation = CarSimulation.from_live_car_data(live_car_data)
        turn_instruction = self.get_turn_instruction(
            live_car_data, track, speed_instruction
        )
        car_control_instructions: CarControlInstructions = {
            "movement_instructions": {
                "turn_instruction": turn_instruction,
                "speed_instruction": speed_instruction,
            },
            "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
        }
        car_simulation.move(car_control_instructions)
        will_go_off_track = self.will_go_off_track(car_simulation, track, 2)
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
                    "movement_instructions": {
                        "speed_instruction": SpeedInstruction.BRAKE,
                        "turn_instruction": self.get_turn_instruction(
                            car_simulation.get_live_data(),
                            track,
                            SpeedInstruction.BRAKE,
                        ),
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
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
        min_velocity: float | None = None,
    ) -> bool:
        """
        Check if car will go off track.
        """
        if min_velocity is None:
            min_velocity = 0
        if car_simulation.velocity < min_velocity:
            return False
        if self.distance_to_track(car_simulation, track) > self.max_distance_to_track:
            return True
        for _ in range(self.simulation_max_future_steps):
            speed_instruction: SpeedInstruction = SpeedInstruction.NO_CHANGE
            if car_simulation.velocity > min_velocity:
                speed_instruction = SpeedInstruction.BRAKE
            elif car_simulation.velocity < min_velocity:
                speed_instruction = SpeedInstruction.ACCELERATE_FRONT
            car_simulation.move(
                {
                    "movement_instructions": {
                        "speed_instruction": speed_instruction,
                        "turn_instruction": self.get_turn_instruction(
                            car_simulation.get_live_data(), track, speed_instruction
                        ),
                    },
                    "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
                }
            )
            if (
                self.distance_to_track(car_simulation, track)
                > self.max_distance_to_track
            ):
                return True
            if (
                abs(
                    self.index_of_closest_track_point(car_simulation, track)
                    - len(track.track_path)
                )
                < 10
            ):
                return False
        return False

    def distance_to_track(self, car_simulation: CarSimulation, track: Track) -> float:
        return track.get_distance_to_point(car_simulation.front_middle)

    def index_of_closest_track_point(
        self, car_simulation: CarSimulation, track: Track
    ) -> int:
        return track.find_index_of_closest_point(car_simulation.front_middle)
