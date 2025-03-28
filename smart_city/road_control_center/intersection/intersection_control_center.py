from car.instruction_controlled_car import CarControlInstructions
from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.intersection.intersection_control_center_software import (
    IntersectionControlCenterSoftware,
)
from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionCarManoeuvreInfo,
)
from smart_city.road_control_center.manoeuvres.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.schemas import LiveCarData


class IntersectionControlCenter(RoadControlCenter):
    def __init__(
        self, intersection: Intersection, intersection_rules: IntersectionRules
    ):
        super().__init__()
        self.software = IntersectionControlCenterSoftware(
            intersection, intersection_rules
        )
        self.intersection = intersection
        self.cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo] = {}

    def calculate_movement_instruction(
        self, registry_number: str
    ) -> CarControlInstructions:
        if registry_number not in self.cars_manoeuvre_info:
            return self.software.get_default_movement_instruction()

        manoeuvre_info = self.cars_manoeuvre_info[registry_number]
        live_car_data = self.live_cars_data[registry_number]
        if manoeuvre_info["manoeuvre_status"]["can_safely_cross_intersection"]:
            return self.software.follow_track_movement_instruction(
                live_car_data, manoeuvre_info["manoeuvre"]
            )
        return self.software.approach_intersection_movement_instruction(
            registry_number, self.live_cars_data, self.cars_manoeuvre_info, self.time
        )

    def update_active_cars_on_road(self, registry_numbers: list[str]) -> None:
        self.cars_manoeuvre_info = {
            registry_number: car_manoeuvre_info
            for registry_number, car_manoeuvre_info in self.cars_manoeuvre_info.items()
            if registry_number in registry_numbers
        }

    def register_new_active_car(self, live_car_data: LiveCarData) -> None:
        manoeuvre_description = live_car_data["manoeuvre_description"]
        manoeuvre = IntersectionManoeuvre(
            live_car_data["specification"]["model"],
            self.intersection,
            manoeuvre_description,
        )
        registry_number = live_car_data["specification"]["registry_number"]
        self.cars_manoeuvre_info[registry_number] = {
            "manoeuvre": manoeuvre,
            "manoeuvre_status": {"can_safely_cross_intersection": False},
        }
