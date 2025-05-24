from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModelSpecification
from schemas import CardinalDirection
from road_segments.intersection.intersection import Intersection
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center_software import (
    IntersectionControlCenterSoftware,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvres_manager import (
    IntersectionManoeuvresManager,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection_control_center.schemas import (
    IntersectionCarManoeuvreInfo,
)
from traffic_control_system.road_control_center.road_control_center import (
    RoadControlCenter,
)
from traffic_control_system.schemas import LiveCarData


class IntersectionControlCenter(RoadControlCenter):
    def __init__(
        self,
        intersection: Intersection,
        intersection_rules: IntersectionRules,
        id: str,
    ):
        super().__init__(intersection, id)
        self.intersection = intersection
        self.intersection_manoeuvres_manager = IntersectionManoeuvresManager(
            intersection
        )
        self.software = IntersectionControlCenterSoftware(
            intersection, intersection_rules
        )
        self.cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo] = {}

    def calculate_control_instructions(
        self, registry_number: str
    ) -> CarControlInstructions:
        if registry_number not in self.cars_manoeuvre_info:
            return self.software.get_default_movement_instruction()

        manoeuvre_info = self.cars_manoeuvre_info[registry_number]
        live_car_data = self.live_cars_data[registry_number]
        if manoeuvre_info["manoeuvre_status"]["can_safely_cross_intersection"]:
            return manoeuvre_info["manoeuvre"].get_car_control_instructions(
                live_car_data
            )
        return self.software.approach_intersection_movement_instruction(
            registry_number, self.live_cars_data, self.cars_manoeuvre_info
        )

    def update_active_cars_on_road(self, registry_numbers: list[str]) -> None:
        self.cars_manoeuvre_info = {
            registry_number: car_manoeuvre_info
            for registry_number, car_manoeuvre_info in self.cars_manoeuvre_info.items()
            if registry_number in registry_numbers
        }

    def register_new_active_car(self, live_car_data: LiveCarData) -> None:
        manoeuvre_description = live_car_data["manoeuvre_description"]
        if not manoeuvre_description:
            manoeuvre_description = {
                "starting_side": CardinalDirection.DOWN,
                "ending_side": CardinalDirection.UP,
            }
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

    def register_car_model(
        self, car_model_specification: CarModelSpecification
    ) -> bool:
        self.intersection_manoeuvres_manager.register_track_velocities(
            car_model_specification
        )
        self.software.add_car_model_tracks(car_model_specification)
        return True

    def register_tracks(self) -> bool:
        self.intersection_manoeuvres_manager.register_tracks()
        return True
