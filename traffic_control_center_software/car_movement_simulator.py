from car.instruction_controlled_car import MovementInstruction, SpeedModifications
from geometry import Rectangle
from smart_city.schemas import LiveCarData
from traffic_control_center_software.car_simulation import CarSimulation
from traffic_control_center_software.schemas import (
    EnteringZoneStatus,
)
from traffic_control_center_software.track import Track
from traffic_control_center_software.track_follower import TrackFollower


def can_stop_before_zone(
    live_car_data: LiveCarData,
    track: Track,
    zone: Rectangle,
    movement_instruction: MovementInstruction | None = None,
) -> bool:
    car_simulation = CarSimulation(live_car_data)
    if movement_instruction:
        car_simulation.apply_movement_instruction(movement_instruction)
        car_simulation.move()
    if car_simulation.collides(zone):
        return False
    while car_simulation.velocity > 0:
        turn_direction = TrackFollower().turning_policy(
            car_simulation.get_live_data(), track
        )
        car_simulation.move(
            movement_decision={
                "turn_direction": turn_direction,
                "speed_modification": SpeedModifications.BRAKE,
            }
        )
        if car_simulation.collides(zone):
            return False
    return True


def get_status_before_entering_zone(
    live_car_data: LiveCarData,
    track: Track,
    zone: Rectangle,
    movement_instruction: MovementInstruction,
) -> EnteringZoneStatus:
    car_simulation = CarSimulation(live_car_data)
    previous_live_car_data = live_car_data
    current_live_car_data = live_car_data
    time = 0
    if movement_instruction:
        car_simulation.apply_movement_instruction(movement_instruction)
        car_simulation.move()
        current_live_car_data = car_simulation.get_live_data()
        time += 1

    while not car_simulation.collides(zone):
        previous_live_car_data = current_live_car_data
        movement_instruction = TrackFollower().get_movement_instruction(
            current_live_car_data, track
        )
        car_simulation.move(movement_instruction)
        current_live_car_data = car_simulation.get_live_data()
        time += 1
    return {"time_to_enter_zone": time, "live_car_data": previous_live_car_data}


def get_predicted_live_car_data(
    live_car_data: LiveCarData, movement_instruction: MovementInstruction
) -> LiveCarData:
    car_simulation = CarSimulation(live_car_data)
    car_simulation.apply_movement_instruction(movement_instruction)
    car_simulation.move()
    return {
        "length": live_car_data["length"],
        "width": live_car_data["width"],
        "direction": car_simulation.direction,
        "front_middle": car_simulation.front_middle,
        "front_right": car_simulation.front_right,
        "front_left": car_simulation.front_left,
        "rear_middle": car_simulation.rear_middle,
        "rear_left": car_simulation.rear_left,
        "rear_right": car_simulation.rear_right,
        "color": live_car_data["color"],
        "model": live_car_data["model"],
        "wheels_angle": car_simulation.wheels_angle,
        "max_acceleration": live_car_data["max_acceleration"],
        "velocity": car_simulation.velocity,
        "max_velocity": live_car_data["max_velocity"],
        "max_brake": live_car_data["max_brake"],
        "registry_number": live_car_data["registry_number"],
        "manoeuvre_description": live_car_data["manoeuvre_description"],
    }
