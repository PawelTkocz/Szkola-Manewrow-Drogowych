from car.instruction_controlled_car import CarControlInstructions, SpeedInstruction
from geometry import Rectangle
from smart_city.road_control_center.manoeuvres.track import Track
from smart_city.road_control_center.software.car_simulation import CarSimulation
from smart_city.road_control_center.software.schemas import EnteringZoneStatus
from smart_city.road_control_center.software.track_follower import TrackFollower
from smart_city.schemas import LiveCarData


def can_stop_before_zone(
    live_car_data: LiveCarData,
    track: Track,
    zone: Rectangle,
    car_control_instructions: CarControlInstructions | None = None,
) -> bool:
    car_simulation = CarSimulation(live_car_data)
    if car_control_instructions:
        car_simulation.move(car_control_instructions)
    if car_simulation.collides(zone):
        return False
    while car_simulation.velocity > 0:
        speed_instruction = SpeedInstruction.BRAKE
        turn_instruction = TrackFollower().get_turn_instruction(
            car_simulation.get_live_data(), track, speed_instruction
        )
        car_simulation.move(
            {
                "speed_instruction": speed_instruction,
                "turn_instruction": turn_instruction,
            }
        )
        if car_simulation.collides(zone):
            return False
    return True


def get_status_before_entering_zone(
    live_car_data: LiveCarData,
    track: Track,
    zone: Rectangle,
    car_control_instructions: CarControlInstructions,
) -> EnteringZoneStatus:
    car_simulation = CarSimulation(live_car_data)
    previous_live_car_data = live_car_data
    current_live_car_data = live_car_data
    time = 0
    if car_control_instructions:
        car_simulation.move(car_control_instructions)
        current_live_car_data = car_simulation.get_live_data()
        time += 1

    while not car_simulation.collides(zone):
        previous_live_car_data = current_live_car_data
        control_instructions = TrackFollower().get_car_control_instructions(
            current_live_car_data, track
        )
        car_simulation.move(control_instructions)
        current_live_car_data = car_simulation.get_live_data()
        time += 1
    return {"time_to_enter_zone": time, "live_car_data": previous_live_car_data}


def get_predicted_live_car_data(
    live_car_data: LiveCarData, car_control_instructions: CarControlInstructions
) -> LiveCarData:
    car_simulation = CarSimulation(live_car_data)
    car_simulation.move(car_control_instructions)
    return car_simulation.get_live_data()
