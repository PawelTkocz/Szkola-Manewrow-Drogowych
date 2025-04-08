from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnSignalsInstruction,
)
from geometry import Point
from smart_city.road_control_center.manoeuvres.schemas import TrackPointData, TurnSignal
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.software.car_simulation import CarSimulation
from smart_city.schemas import LiveCarData


class ManoeuvrePhase:
    """
    Class representing one phase of a manoeuvre.
    """

    def __init__(
        self,
        track_points_data: list[TrackPointData],
    ):
        self.track = Track(
            [
                (point_data["point"].x, point_data["point"].y)
                for point_data in track_points_data
            ]
        )
        self.max_safe_velocities = [
            point_data["max_safe_velocity"] for point_data in track_points_data
        ]
        self.turn_signals = [
            point_data["turn_signal"] for point_data in track_points_data
        ]

    def get_car_control_instructions(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions:
        track_point_index = self.track.find_index_of_closest_point(
            live_car_data["live_state"]["front_middle"]
        )
        max_safe_velocity = self.max_safe_velocities[track_point_index]
        current_velocity = live_car_data["live_state"]["velocity"]
        speed_instruction = SpeedInstruction.NO_CHANGE
        if current_velocity > max_safe_velocity:
            speed_instruction = SpeedInstruction.BRAKE
        elif (
            current_velocity + live_car_data["specification"]["model"].max_acceleration
            < max_safe_velocity
        ):
            speed_instruction = SpeedInstruction.ACCELERATE_FRONT
        turn_signal = self.turn_signals[track_point_index]
        turn_signal_instruction = TurnSignalsInstruction.NO_SIGNALS_ON
        if turn_signal == TurnSignal.LEFT_SIGNAL:
            turn_signal_instruction = TurnSignalsInstruction.LEFT_SIGNAL_ON
        elif turn_signal == TurnSignal.RIGHT_SIGNAL:
            turn_signal_instruction = TurnSignalsInstruction.RIGHT_SIGNAL_ON

        return {
            "movement_instructions": {
                "speed_instruction": speed_instruction,
                "turn_instruction": CarSimulation.from_live_car_data(
                    live_car_data
                ).get_turn_instruction(self.track, speed_instruction),
            },
            "turn_signals_instruction": turn_signal_instruction,
        }

    def is_phase_over(self, front_middle_position: Point, velocity: float) -> bool:
        return False
