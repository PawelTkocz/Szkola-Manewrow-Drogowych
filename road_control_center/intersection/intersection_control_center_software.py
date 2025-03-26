from typing import TypedDict
from car.instruction_controlled_car import MovementInstruction, SpeedModifications
from geometry import Directions
from manoeuvres.intersection_manoeuvre import IntersectionManoeuvre
from road_control_center.intersection.intersection_rules import IntersectionRules
from road_control_center.intersection.schemas import (
    IntersectionCarManoeuvreInfo,
)
from road_segments.intersection.intersection import Intersection
from smart_city.schemas import LiveCarData
from traffic_control_center_software.car_movement_simulator import (
    can_stop_before_zone,
    get_status_before_entering_zone,
)
from traffic_control_center_software.car_simulation import CarSimulation
from traffic_control_center_software.track_follower import TrackFollower


class CarOnIntersectionSimulation(TypedDict):
    car_simulation: CarSimulation
    car_manoeuvre_info: IntersectionCarManoeuvreInfo


class IntersectionControlCenterSoftware:
    def __init__(
        self, intersection: Intersection, intersection_rules: IntersectionRules
    ):
        self.intersection = intersection
        self.intersection_rules = intersection_rules
        self.track_follower = TrackFollower()

    def get_default_movement_instruction(self) -> MovementInstruction:
        return {
            "speed_modification": SpeedModifications.NO_CHANGE,
            "turn_direction": Directions.FRONT,
        }

    def follow_track_movement_instruction(
        self, live_car_data: LiveCarData, manoeuvre: IntersectionManoeuvre
    ) -> MovementInstruction:
        desired_end_state = manoeuvre.phases[0].desired_end_state
        track = manoeuvre.phases[0].track
        return self.track_follower.get_movement_instruction(
            live_car_data, track, desired_end_state
        )

    def approach_intersection_movement_instruction(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> MovementInstruction:
        # first just follow track, then validate
        movement_instructions: list[MovementInstruction] = [
            {
                "speed_modification": speed_modification,
                "turn_direction": self.track_follower.get_best_turn_direction(
                    speed_modification
                ),
            }
            for speed_modification in [
                SpeedModifications.SPEED_UP,
                SpeedModifications.NO_CHANGE,
            ]
        ]
        for movement_instruction in movement_instructions:
            if self.is_approaching_instruction_safe(
                registry_number,
                live_cars_data,
                movement_instruction,
                cars_manoeuvre_info,
                time,
            ):
                return movement_instruction
        return {
            "speed_modification": SpeedModifications.BRAKE,
            "turn_direction": self.track_follower.get_best_turn_direction(
                SpeedModifications.BRAKE
            ),
        }

    def is_approaching_instruction_safe(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        movement_instruction: MovementInstruction,
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> bool:
        live_car_data = live_cars_data[registry_number]
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        if can_stop_before_zone(
            live_car_data,
            manoeuvre_info["manoeuvre"].phases[0].track,
            self.intersection.intersection_parts["intersection_area"],
            movement_instruction,
        ):
            return True
        return self.can_safely_cross_the_intersection(
            registry_number,
            live_cars_data,
            movement_instruction,
            cars_manoeuvre_info,
            time,
        )

    def can_safely_cross_the_intersection(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        movement_instruction: MovementInstruction,
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> bool:
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        live_car_data = live_cars_data[registry_number]
        track = manoeuvre_info["manoeuvre"].phases[0].track
        entering_intersection_status = get_status_before_entering_zone(
            live_car_data,
            track,
            self.intersection.intersection_parts["intersection_area"],
            movement_instruction,
        )
        entering_intersection_time = (
            entering_intersection_status["time_to_enter_zone"] + time
        )
        entering_intersection_live_car_data = entering_intersection_status[
            "live_car_data"
        ]
        if not self.intersection_rules.can_enter_intersection(
            {
                "live_car_data": entering_intersection_live_car_data,
                "manoeuvre_description": manoeuvre_info[
                    "manoeuvre"
                ].manoeuvre_description,
            },
            entering_intersection_time,
        ):
            return False

        cars_with_priority = self.get_cars_with_priority(
            registry_number,
            entering_intersection_time,
            live_cars_data,
            cars_manoeuvre_info,
        )
        return self.can_cross_intersection_without_priority_violation(
            registry_number,
            cars_with_priority,
            live_cars_data,
            cars_manoeuvre_info,
            movement_instruction,
        )

    def get_cars_with_priority(
        self,
        registry_number: str,
        time: int,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
    ) -> list[str]:
        return [
            _registry_number
            for _registry_number, car_manoeuvre_info in cars_manoeuvre_info.items()
            if _registry_number != registry_number
            and self.intersection_rules.has_priority(
                {
                    "live_car_data": live_cars_data[_registry_number],
                    "manoeuvre_description": car_manoeuvre_info[
                        "manoeuvre"
                    ].manoeuvre_description,
                },
                {
                    "live_car_data": live_cars_data[registry_number],
                    "manoeuvre_description": cars_manoeuvre_info[registry_number][
                        "manoeuvre"
                    ].manoeuvre_description,
                },
                time,
            )
        ]

    def can_cross_intersection_without_priority_violation(
        self,
        registry_number: str,
        cars_with_priority: list[str],
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        movement_instruction: MovementInstruction,
    ) -> bool:
        if not cars_with_priority:
            return True
        priority_cars: list[CarOnIntersectionSimulation] = [
            {
                "car_simulation": CarSimulation(live_cars_data[_registry_number]),
                "car_manoeuvre_info": cars_manoeuvre_info[_registry_number],
            }
            for _registry_number in cars_with_priority
        ]
        priority_cars_crossing_intersection = [
            car for car in priority_cars if self.is_car_crossing_intersection(car)
        ]
        priority_cars_closing_to_intersection = [
            car
            for car in priority_cars
            if car not in priority_cars_crossing_intersection
        ]
        car_simulation: CarOnIntersectionSimulation = {
            "car_simulation": CarSimulation(live_cars_data[registry_number]),
            "car_manoeuvre_info": cars_manoeuvre_info[registry_number],
        }
        car_simulation["car_simulation"].apply_movement_instruction(
            movement_instruction
        )
        car_simulation["car_simulation"].move()
        for car in priority_cars:
            self._move_car_simulation(car)
        # if at least one car closing to intersetion would enter the intersection, you CAN'T go
        # if you would get to close to any of cars already on intersection, you CAN'T go
        while not self.has_car_crossed_intersection(car_simulation):
            if self._priority_violation(
                car_simulation,
                priority_cars_crossing_intersection,
                priority_cars_closing_to_intersection,
            ):
                return False
            for car in priority_cars + [car_simulation]:
                self._move_car_simulation(car)
        return True

    def is_car_crossing_intersection(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ) -> bool:
        car_simulation = intersection_car_simulation["car_simulation"]
        manoeuvre_description = intersection_car_simulation["car_manoeuvre_info"][
            "manoeuvre"
        ].manoeuvre_description
        intersection = intersection_car_simulation["car_manoeuvre_info"][
            "manoeuvre"
        ].intersection
        intersection_area = intersection.intersection_parts["intersection_area"]
        outcoming_lane = intersection.intersection_parts["outcoming_lines"][
            manoeuvre_description["ending_side"]
        ]
        return car_simulation.collides(intersection_area) or car_simulation.collides(
            outcoming_lane
        )

    def has_car_crossed_intersection(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ) -> bool:
        car_simulation = intersection_car_simulation["car_simulation"]
        manoeuvre_description = intersection_car_simulation["car_manoeuvre_info"][
            "manoeuvre"
        ].manoeuvre_description
        intersection = intersection_car_simulation["car_manoeuvre_info"][
            "manoeuvre"
        ].intersection
        intersection_area = intersection.intersection_parts["intersection_area"]
        outcoming_lane = intersection.intersection_parts["outcoming_lines"][
            manoeuvre_description["ending_side"]
        ]
        return not car_simulation.collides(
            intersection_area
        ) and car_simulation.collides(outcoming_lane)

    def _move_car_simulation(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ):
        manoeuvre = intersection_car_simulation["car_manoeuvre_info"]["manoeuvre"]
        car_simulation = intersection_car_simulation["car_simulation"]
        track = manoeuvre.phases[0].track
        end_state = manoeuvre.phases[0].desired_end_state
        movement_instruction = TrackFollower().get_movement_instruction(
            car_simulation.get_live_data(), track, end_state
        )
        car_simulation.apply_movement_instruction(movement_instruction)
        car_simulation.move()

    def _priority_violation(
        self,
        car: CarOnIntersectionSimulation,
        priority_cars_crossing_intersection: list[CarOnIntersectionSimulation],
        priority_cars_closing_to_intersection: list[CarOnIntersectionSimulation],
    ) -> bool:
        intersection = car["car_manoeuvre_info"]["manoeuvre"].intersection
        intersection_area = intersection.intersection_parts["intersection_area"]
        return any(
            car["car_simulation"].collides(intersection_area)
            for car in priority_cars_closing_to_intersection
        ) or any(
            car_["car_simulation"].collides(car)
            for car_ in priority_cars_crossing_intersection
        )
