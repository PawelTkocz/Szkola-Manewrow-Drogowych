from car.instruction_controlled_car import (
    CarMovementInstructions,
    SpeedInstruction,
    TurnInstruction,
)
from smart_city.road_control_center.track import Track
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
                "speed_instruction": speed_instruction,
                "turn_instruction": turn_instruction,
            },
        )
        return track.get_distance_to_point(car_simulation.front_middle)

    if live_car_data["live_state"]["velocity"] == 0:
        return TurnInstruction.NO_CHANGE
    return min(TurnInstruction, key=_distance_to_track_after_turn)


def get_predicted_live_car_data(
    live_car_data: LiveCarData, movement_instructions: CarMovementInstructions
) -> LiveCarData:
    car_simulation = CarSimulation.from_live_car_data(live_car_data)
    car_simulation.move(movement_instructions)
    return car_simulation.get_live_data()
