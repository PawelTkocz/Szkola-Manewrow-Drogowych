from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnSignalsInstruction,
)
from geometry.shapes.rectangle import Rectangle
from smart_city.road_control_center.manoeuvres_preprocessing.schemas import (
    EnteringZoneStatus,
    ManoeuvreTrackPoint,
    TurnSignal,
)
from smart_city.road_control_center.track import Track
from smart_city.road_control_center.utils import (
    get_turn_instruction,
)
from smart_city.road_control_center.car_simulation import CarSimulation
from smart_city.schemas import LiveCarData


class PreprocessedManoeuvre:
    """
    Class representing preporcessed manoeuvre.
    """

    def __init__(
        self,
        manoeuvre_track_points: list[ManoeuvreTrackPoint],
    ):
        self.track = Track(
            [point_data["point"].to_tuple() for point_data in manoeuvre_track_points]
        )
        self.max_safe_velocities = [
            point_data["max_safe_velocity"] for point_data in manoeuvre_track_points
        ]
        self.turn_signals = [
            point_data["turn_signal"] for point_data in manoeuvre_track_points
        ]

    def get_all_car_control_instructions(
        self, live_car_data: LiveCarData
    ) -> list[CarControlInstructions]:
        track_point_index = self.track.find_index_of_closest_point(
            live_car_data["live_state"]["front_middle"]
        )
        turn_signal_instruction = self._get_turn_singal_instruction(track_point_index)
        speed_instruction = self._get_speed_instruction(
            track_point_index, live_car_data
        )
        speed_instructions = [
            SpeedInstruction.ACCELERATE_FRONT,
            SpeedInstruction.NO_CHANGE,
            SpeedInstruction.BRAKE,
        ]
        speed_instruction_index = speed_instructions.index(speed_instruction)
        safe_car_control_instructions: list[CarControlInstructions] = []
        for speed_instruction in speed_instructions[speed_instruction_index:]:
            safe_car_control_instructions.append(
                {
                    "movement_instructions": {
                        "speed_instruction": speed_instruction,
                        "turn_instruction": get_turn_instruction(
                            self.track, live_car_data, speed_instruction
                        ),
                    },
                    "turn_signals_instruction": turn_signal_instruction,
                }
            )
        return safe_car_control_instructions

    def get_car_control_instructions(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions:
        track_point_index = self.track.find_index_of_closest_point(
            live_car_data["live_state"]["front_middle"]
        )
        speed_instruction = self._get_speed_instruction(
            track_point_index, live_car_data
        )
        turn_signal_instruction = self._get_turn_singal_instruction(track_point_index)

        return {
            "movement_instructions": {
                "speed_instruction": speed_instruction,
                "turn_instruction": get_turn_instruction(
                    self.track, live_car_data, speed_instruction
                ),
            },
            "turn_signals_instruction": turn_signal_instruction,
        }

    def _get_speed_instruction(
        self, track_point_index: int, live_car_data: LiveCarData
    ) -> SpeedInstruction:
        max_safe_velocity = self.max_safe_velocities[track_point_index]
        current_velocity = live_car_data["live_state"]["velocity"]
        speed_instruction = SpeedInstruction.NO_CHANGE
        if current_velocity > max_safe_velocity:
            speed_instruction = SpeedInstruction.BRAKE
        elif (
            current_velocity
            + live_car_data["specification"]["model"]["motion"]["acceleration"]
            < max_safe_velocity
        ):
            speed_instruction = SpeedInstruction.ACCELERATE_FRONT
        return speed_instruction

    def _get_turn_singal_instruction(
        self, track_point_index: int
    ) -> TurnSignalsInstruction:
        turn_signal = self.turn_signals[track_point_index]
        turn_signal_instruction = TurnSignalsInstruction.NO_SIGNALS_ON
        if turn_signal == TurnSignal.LEFT_SIGNAL:
            turn_signal_instruction = TurnSignalsInstruction.LEFT_SIGNAL_ON
        elif turn_signal == TurnSignal.RIGHT_SIGNAL:
            turn_signal_instruction = TurnSignalsInstruction.RIGHT_SIGNAL_ON
        return turn_signal_instruction

    def can_stop_before_zone(
        self,
        live_car_data: LiveCarData,
        zone: Rectangle,
        *,
        car_control_instructions: CarControlInstructions | None = None,
    ) -> bool:
        car_simulation = CarSimulation.from_live_car_data(live_car_data)
        if car_control_instructions:
            car_simulation.move(car_control_instructions["movement_instructions"])
        if car_simulation.collides(zone):
            return False
        while car_simulation.velocity > 0:
            speed_instruction = SpeedInstruction.BRAKE
            turn_instruction = get_turn_instruction(
                self.track, car_simulation.get_live_data(), speed_instruction
            )
            car_simulation.move(
                {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": turn_instruction,
                },
            )
            if car_simulation.collides(zone):
                return False
        return True

    def get_status_before_entering_zone(
        self,
        live_car_data: LiveCarData,
        zone: Rectangle,
        *,
        car_control_instructions: CarControlInstructions,
    ) -> EnteringZoneStatus:
        car_simulation = CarSimulation.from_live_car_data(live_car_data)
        previous_live_car_data = live_car_data
        current_live_car_data = live_car_data
        time = 0
        if car_control_instructions:
            car_simulation.move(car_control_instructions["movement_instructions"])
            current_live_car_data = car_simulation.get_live_data()
            time += 1

        while not car_simulation.collides(zone):
            previous_live_car_data = current_live_car_data
            control_instructions = self.get_car_control_instructions(
                current_live_car_data
            )
            car_simulation.move(control_instructions["movement_instructions"])
            current_live_car_data = car_simulation.get_live_data()
            time += 1
        return {"time_to_enter_zone": time, "live_car_data": previous_live_car_data}
