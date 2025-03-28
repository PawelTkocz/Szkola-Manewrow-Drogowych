from typing import TypedDict
from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
)

from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionCarManoeuvreInfo,
)
from smart_city.road_control_center.manoeuvres.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from smart_city.road_control_center.software.car_movement_simulator import (
    can_stop_before_zone,
    get_status_before_entering_zone,
)
from smart_city.road_control_center.software.car_simulation import CarSimulation
from smart_city.road_control_center.software.track_follower import TrackFollower
from smart_city.schemas import LiveCarData


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

    def get_default_movement_instruction(self) -> CarControlInstructions:
        return {
            "speed_instruction": SpeedInstruction.NO_CHANGE,
            "turn_instruction": TurnInstruction.NO_CHANGE,
        }

    def follow_track_movement_instruction(
        self, live_car_data: LiveCarData, manoeuvre: IntersectionManoeuvre
    ) -> CarControlInstructions:
        current_phase = manoeuvre.get_current_phase()
        if not current_phase:
            return self.get_default_movement_instruction()
        track = current_phase.track
        stop_point = current_phase.stop_point
        return self.track_follower.get_car_control_instructions(
            live_car_data, track, stop_point
        )

    def approach_intersection_movement_instruction(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> CarControlInstructions:
        live_car_data = live_cars_data[registry_number]
        valid_speed_instructions = self.track_follower.get_valid_speed_instructions(
            live_car_data["live_state"]["velocity"]
        )
        current_phase = cars_manoeuvre_info[registry_number][
            "manoeuvre"
        ].get_current_phase()
        if not current_phase:
            return self.get_default_movement_instruction()
        track = current_phase.track
        stop_point = current_phase.stop_point
        for speed_instruction in valid_speed_instructions[:-1]:
            if not self.track_follower.is_speed_instruction_safe(
                live_car_data, track, stop_point, speed_instruction
            ):
                continue
            car_control_instructions: CarControlInstructions = {
                "speed_instruction": speed_instruction,
                "turn_instruction": self.track_follower.get_turn_instruction(
                    live_car_data, track, speed_instruction
                ),
            }
            if self.is_approaching_instruction_safe(
                registry_number,
                live_cars_data,
                car_control_instructions,
                cars_manoeuvre_info,
                time,
            ):
                return car_control_instructions
        return {
            "speed_instruction": valid_speed_instructions[-1],
            "turn_instruction": self.track_follower.get_turn_instruction(
                live_car_data, track, valid_speed_instructions[-1]
            ),
        }

    def is_approaching_instruction_safe(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        car_control_instructions: CarControlInstructions,
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> bool:
        live_car_data = live_cars_data[registry_number]
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        current_phase = manoeuvre_info["manoeuvre"].get_current_phase()
        if not current_phase:
            return False
        track = current_phase.track
        if can_stop_before_zone(
            live_car_data,
            track,
            self.intersection.intersection_parts["intersection_area"],
            car_control_instructions,
        ):
            return True
        return self.can_safely_cross_the_intersection(
            registry_number,
            live_cars_data,
            car_control_instructions,
            cars_manoeuvre_info,
            time,
        )

    def can_safely_cross_the_intersection(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        car_control_instructions: CarControlInstructions,
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> bool:
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        live_car_data = live_cars_data[registry_number]
        current_phase = manoeuvre_info["manoeuvre"].get_current_phase()
        if not current_phase:
            return False
        track = current_phase.track
        entering_intersection_status = get_status_before_entering_zone(
            live_car_data,
            track,
            self.intersection.intersection_parts["intersection_area"],
            car_control_instructions,
        )
        entering_intersection_time = (
            entering_intersection_status["time_to_enter_zone"] + time
        )
        entering_intersection_live_car_data = entering_intersection_status[
            "live_car_data"
        ]
        if not self.intersection_rules.can_enter_intersection(
            {
                "manoeuvre_description": manoeuvre_info[
                    "manoeuvre"
                ].manoeuvre_description,
                "high_priority": entering_intersection_live_car_data["live_state"][
                    "high_priority"
                ],
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
            car_control_instructions,
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
                    "high_priority": live_cars_data[_registry_number]["live_state"][
                        "high_priority"
                    ],
                    "manoeuvre_description": car_manoeuvre_info[
                        "manoeuvre"
                    ].manoeuvre_description,
                },
                {
                    "high_priority": live_cars_data[registry_number]["live_state"][
                        "high_priority"
                    ],
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
        car_control_instructions: CarControlInstructions,
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
        car_simulation["car_simulation"].move(car_control_instructions)
        for car in priority_cars:
            self._move_car_simulation(car)
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
        intersection_area = self.intersection.intersection_parts["intersection_area"]
        outcoming_lane = self.intersection.intersection_parts["outcoming_lines"][
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
        intersection_area = self.intersection.intersection_parts["intersection_area"]
        outcoming_lane = self.intersection.intersection_parts["outcoming_lines"][
            manoeuvre_description["ending_side"]
        ]
        return not car_simulation.collides(
            intersection_area
        ) and car_simulation.collides(outcoming_lane)

    def _move_car_simulation(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ) -> None:
        manoeuvre = intersection_car_simulation["car_manoeuvre_info"]["manoeuvre"]
        car_simulation = intersection_car_simulation["car_simulation"]
        car_control_instructions = self.follow_track_movement_instruction(
            car_simulation.get_live_data(), manoeuvre
        )
        car_simulation.move(car_control_instructions)

    def _priority_violation(
        self,
        car: CarOnIntersectionSimulation,
        priority_cars_crossing_intersection: list[CarOnIntersectionSimulation],
        priority_cars_closing_to_intersection: list[CarOnIntersectionSimulation],
    ) -> bool:
        intersection_area = self.intersection.intersection_parts["intersection_area"]
        return any(
            car["car_simulation"].collides(intersection_area)
            for car in priority_cars_closing_to_intersection
        ) or any(
            car_["car_simulation"].collides(car["car_simulation"].car)
            for car_ in priority_cars_crossing_intersection
        )
