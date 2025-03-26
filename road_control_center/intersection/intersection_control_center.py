from abc import abstractmethod
from car.instruction_controlled_car import MovementInstruction, SpeedModifications
from geometry import Directions
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from road_control_center.intersection.intersection_control_center_software import (
    can_cross_intersection_without_priority_violation,
)
from road_control_center.intersection.schemas import (
    IntersectionCarManoeuvreInfo,
    IntersectionManoeuvreDescription,
)
from road_control_center.road_control_center import RoadControlCenter
from road_segments.intersection.intersection import Intersection
from smart_city.schemas import LiveCarData
from traffic_control_center_software.car_movement_simulator import (
    can_stop_before_zone,
    get_predicted_live_car_data,
    get_status_before_entering_zone,
)

from traffic_control_center_software.track_follower import TrackFollower


class IntersectionControlCenter(RoadControlCenter):
    def __init__(self, intersection: Intersection):
        super().__init__()
        self.intersection = intersection
        self.cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo] = {}
        self.track_follower = TrackFollower()

    def _get_movement_instruction(self, registry_number: str) -> MovementInstruction:
        if registry_number not in self.cars_manoeuvre_info:
            return {
                "speed_modification": SpeedModifications.NO_CHANGE,
                "turn_direction": Directions.FRONT,
            }
        manoeuvre_info = self.cars_manoeuvre_info[registry_number]
        manoeuvre = manoeuvre_info["manoeuvre"]
        manoeuvre_status = manoeuvre_info["manoeuvre_status"]
        live_car_data = self._live_cars_data[registry_number]
        if manoeuvre_status["can_safely_cross_intersection"]:
            desired_end_state = manoeuvre.phases[0].desired_end_state
            track = manoeuvre.phases[0].track
            return self.track_follower.get_movement_instruction(
                live_car_data, track, desired_end_state
            )

        # we know that the car still didn't enter the intersection
        turn_direction = self.track_follower.turning_policy(
            live_car_data, track, desired_end_state
        )
        speed_modifications = [
            SpeedModifications.SPEED_UP,
            SpeedModifications.NO_CHANGE,
        ]
        for speed_modification in speed_modifications:
            movement_instruction: MovementInstruction = {
                "speed_modification": speed_modification,
                "turn_direction": turn_direction
            }
            predicted_live_car_data = get_predicted_live_car_data(live_car_data, movement_instruction)
            if can_stop_before_zone(
                predicted_live_car_data,
                manoeuvre.phases[0].track,
                self.intersection.intersection_parts["intersection_area"],
            ):
                return {
                    "speed_modification": speed_modification,
                    "turn_direction": turn_direction,
                }
            if self.can_safely_cross_the_intersection(predicted_live_car_data, self.cars_manoeuvre_info[registry_number]):

        return {
            "speed_modification": SpeedModifications.BRAKE,
            "turn_direction": turn_direction,
        }

    @abstractmethod
    def can_enter_intersection(
        self, intersection_side: Directions, car_velocity: float, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign and so on)"""
        raise NotImplementedError

    @abstractmethod
    def has_priority(
        car1_manoeurve_description: IntersectionManoeuvreDescription,
        car2_manoeuvre_description: IntersectionManoeuvreDescription,
        time: int,
    ) -> bool:
        raise NotImplementedError

    def get_cars_with_priority(
        self, car_manoeuvre_info: CarOnIntersection, time: int
    ) -> list[CarOnIntersection]:
        return [
            intersection_car
            for intersection_car in self.cars_manoeuvre_info
            if intersection_car is not car
            and self.has_priority(
                intersection_car["manoeuvre_description"],
                car["manoeuvre_description"],
                time,
            )
        ]

    def can_safely_cross_the_intersection(self, live_car_data: LiveCarData, manoeuvre_info: IntersectionCarManoeuvreInfo) -> bool:
        track = manoeuvre_info["manoeuvre"].phases[0].track
        entering_intersection_status = get_status_before_entering_zone(
            live_car_data,
            track,
            self.intersection.intersection_parts["intersection_area"],
        )
        time_to_enter_intersection = entering_intersection_status["time_to_enter_zone"]
        entering_intersection_live_car_data = entering_intersection_status[
            "live_car_data"
        ]
        if not self.can_enter_intersection(
            manoeuvre_info["manoeuvre"].manoeuvre_description["starting_side"],
            entering_intersection_live_car_data["velocity"],
            self._time + time_to_enter_intersection,
        ):
            return False

        cars_with_priority = self.get_cars_with_priority(
            car, self._time + time_to_enter_intersection
        )
        return can_cross_intersection_without_priority_violation(
            car, cars_with_priority
        )

    def _handle_cars_that_left_the_road(self, cars_registry_numbers: list[str]) -> None:
        self.cars_manoeuvre_info = {
            registry_number: car_manoeuvre_info
            for registry_number, car_manoeuvre_info in self.cars_manoeuvre_info.items()
            if registry_number not in cars_registry_numbers
        }

    def _add_new_car_on_road(self, live_car_data: LiveCarData) -> None:
        manoeuvre_description = live_car_data["manoeuvre_description"]
        manoeuvre = IntersectionManoeuvre(
            live_car_data["model"], self.intersection, manoeuvre_description
        )
        registry_number = live_car_data["registry_number"]
        self.cars_manoeuvre_info[registry_number] = {
            "manoeuvre": manoeuvre,
            "manoeuvre_status": {"can_safely_cross_intersection": False},
        }
