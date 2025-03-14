from car.autonomous_car import LiveCarData
from geometry import Rectangle
from traffic_control_center_software.car_simulation import CarSimulation
from traffic_control_center_software.schemas import EnteringZoneStatus, SpeedModifications
from traffic_control_center_software.track import Track
from traffic_control_center_software.track_follower import TrackFollower


def can_stop_before_zone(live_car_data: LiveCarData, track: Track, zone: Rectangle) -> bool:
    car_simulation = CarSimulation(live_car_data)
    if car_simulation.collides(zone):
        return False
    while car_simulation.velocity > 0:
        turn_direction = TrackFollower().turning_policy(car_simulation.get_live_data(), track)
        car_simulation.move(movement_decision={"turn_direction": turn_direction, "speed_modification": SpeedModifications.BRAKE})
        if car_simulation.collides(zone):
            return False
    return True

def get_status_before_entering_zone(live_car_data: LiveCarData, track: Track, zone: Rectangle) -> EnteringZoneStatus:
    car_simulation = CarSimulation(live_car_data)
    if car_simulation.collides(zone):
        return {"time_needed": 0, "velocity": car_simulation.velocity}
    time = 0
    for _ in range(10):
        time += 1
        movement_instruction = TrackFollower().get_movement_instruction(car_simulation.get_live_data(), track)
        car_simulation.move(movement_instruction)
        if car_simulation.collides(zone):
            break
    return {"time_needed": time, "velocity": car_simulation.velocity}