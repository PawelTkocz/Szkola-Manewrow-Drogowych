from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.car_simulation import CarSimulation
from smart_city.schemas import LiveCarData


def get_turn_instruction(
    track: Track, live_car_data: LiveCarData, speed_instruction: SpeedInstruction
) -> TurnInstruction:
    def _distance_to_track_after_turn(
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
        return track.get_distance_to_point(car_simulation.front_middle)

    if live_car_data["live_state"]["velocity"] == 0:
        return TurnInstruction.NO_CHANGE
    return min(TurnInstruction, key=_distance_to_track_after_turn)


def get_predicted_live_car_data(
    live_car_data: LiveCarData, car_control_instructions: CarControlInstructions
) -> LiveCarData:
    car_simulation = CarSimulation.from_live_car_data(live_car_data)
    car_simulation.move(car_control_instructions)
    return car_simulation.get_live_data()
