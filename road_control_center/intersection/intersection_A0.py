from geometry import Directions
from road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from road_control_center.intersection.schemas import CarOnIntersection
from road_segments.intersection.intersection_A0 import IntersectionA0
from traffic_control_center_software.schemas import MovementInstruction


class IntersectionA0ControlCenter(IntersectionControlCenter):
    def __init__(self):
        super().__init__(IntersectionA0())

    def has_priority(car1: CarOnIntersection, car2: CarOnIntersection) -> bool:
        directions = [Directions.DOWN, Directions.RIGHT, Directions.UP, Directions.LEFT]
        starting_side_index = directions.index(car1["starting_side"])
        direction_index = (starting_side_index + 1) % 4
        while directions[direction_index] != car1["ending_side"]:
            if directions[direction_index] == car2["starting_side"]:
                return False
            direction_index = (direction_index + 1) % 4
        return True

    def get_movement_instructions(self) -> dict[str, MovementInstruction]:
        """Movement instruction for each registry number in cars_data"""
        live_cars_data = [
            car_on_intersection["car_data_transmitter"].get_live_car_data()
            for car_on_intersection in self.cars_data
        ]
