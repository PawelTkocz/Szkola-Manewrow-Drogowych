from typing import TypedDict
from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)

from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from smart_city.road_control_center.intersection.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionCarManoeuvreInfo,
)

from smart_city.road_control_center.utils import (
    get_turn_instruction,
)
from smart_city.road_control_center.car_simulation import CarSimulation
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

    def get_default_movement_instruction(self) -> CarControlInstructions:
        return {
            "movement_instructions": {
                "speed_instruction": SpeedInstruction.NO_CHANGE,
                "turn_instruction": TurnInstruction.NO_CHANGE,
            },
            "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
        }

    def follow_track_movement_instruction(
        self, live_car_data: LiveCarData, manoeuvre: IntersectionManoeuvre
    ) -> CarControlInstructions:
        return manoeuvre.get_car_control_instructions(live_car_data)

    def approach_intersection_movement_instruction(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
        time: int,
    ) -> CarControlInstructions:
        live_car_data = live_cars_data[registry_number]
        manoeuvre = cars_manoeuvre_info[registry_number]["manoeuvre"]
        car_control_instructions = manoeuvre.get_car_control_instructions(live_car_data)
        safe_speed_instruction = car_control_instructions["movement_instructions"][
            "speed_instruction"
        ]
        speed_instructions = [
            SpeedInstruction.ACCELERATE_FRONT,
            SpeedInstruction.NO_CHANGE,
            SpeedInstruction.BRAKE,
        ]
        speed_instruction_index = speed_instructions.index(safe_speed_instruction)
        for speed_instruction in speed_instructions[speed_instruction_index:-1]:
            car_control_instructions = {
                "movement_instructions": {
                    "speed_instruction": speed_instruction,
                    "turn_instruction": get_turn_instruction(
                        manoeuvre.track, live_car_data, speed_instruction
                    ),
                },
                "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
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
            "movement_instructions": {
                "speed_instruction": SpeedInstruction.BRAKE,
                "turn_instruction": get_turn_instruction(
                    manoeuvre.track, live_car_data, SpeedInstruction.BRAKE
                ),
            },
            "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
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
        if manoeuvre_info["manoeuvre"].can_stop_before_zone(
            live_car_data,
            self.intersection.intersection_parts["intersection_area"],
            car_control_instructions=car_control_instructions,
        ):
            return True
        can_safely_cross_the_intersection = self.can_safely_cross_the_intersection(
            registry_number,
            live_cars_data,
            car_control_instructions,
            cars_manoeuvre_info,
            time,
        )
        cars_manoeuvre_info[registry_number]["manoeuvre_status"][
            "can_safely_cross_intersection"
        ] = can_safely_cross_the_intersection
        return can_safely_cross_the_intersection

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
        entering_intersection_status = manoeuvre_info[
            "manoeuvre"
        ].get_status_before_entering_zone(
            live_car_data,
            self.intersection.intersection_parts["intersection_area"],
            car_control_instructions=car_control_instructions,
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
                "velocity": entering_intersection_live_car_data["live_state"][
                    "velocity"
                ],
                "traffic_lights_state": self.intersection.traffic_lights.get_lights_states()
                if self.intersection.traffic_lights
                else {},
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
            and self.intersection_rules.must_yield_the_right_of_way(
                {
                    "high_priority": live_cars_data[registry_number]["live_state"][
                        "high_priority"
                    ],
                    "manoeuvre_description": cars_manoeuvre_info[registry_number][
                        "manoeuvre"
                    ].manoeuvre_description,
                    "velocity": live_cars_data[registry_number]["live_state"][
                        "velocity"
                    ],
                    "traffic_lights_state": self.intersection.traffic_lights.get_lights_states()
                    if self.intersection.traffic_lights
                    else {},
                },
                {
                    "high_priority": live_cars_data[_registry_number]["live_state"][
                        "high_priority"
                    ],
                    "manoeuvre_description": car_manoeuvre_info[
                        "manoeuvre"
                    ].manoeuvre_description,
                    "velocity": live_cars_data[_registry_number]["live_state"][
                        "velocity"
                    ],
                    "traffic_lights_state": self.intersection.traffic_lights.get_lights_states()
                    if self.intersection.traffic_lights
                    else {},
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
                "car_simulation": CarSimulation.from_live_car_data(
                    live_cars_data[_registry_number]
                ),
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
            "car_simulation": CarSimulation.from_live_car_data(
                live_cars_data[registry_number]
            ),
            "car_manoeuvre_info": cars_manoeuvre_info[registry_number],
        }
        car_simulation["car_simulation"].move(
            car_control_instructions["movement_instructions"]
        )
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
        outcoming_lane = self.intersection.intersection_parts["outcoming_lanes"][
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
        outcoming_lane = self.intersection.intersection_parts["outcoming_lanes"][
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
        car_simulation.move(car_control_instructions["movement_instructions"])

    def _priority_violation(
        self,
        car: CarOnIntersectionSimulation,
        priority_cars_crossing_intersection: list[CarOnIntersectionSimulation],
        priority_cars_closing_to_intersection: list[CarOnIntersectionSimulation],
    ) -> bool:
        intersection_area = self.intersection.intersection_parts["intersection_area"]
        return (
            any(
                car["car_simulation"].collides(intersection_area)
                for car in priority_cars_closing_to_intersection
            )
            or any(
                car_["car_simulation"].collides(car["car_simulation"].body)
                for car_ in priority_cars_crossing_intersection
            )
            or any(
                car["car_simulation"].collides(
                    self.intersection.intersection_parts["incoming_lanes"][
                        car["car_manoeuvre_info"]["manoeuvre"].manoeuvre_description[
                            "starting_side"
                        ]
                    ]
                )
                for car in priority_cars_crossing_intersection
            )
        )
