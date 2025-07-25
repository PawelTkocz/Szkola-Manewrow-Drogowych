from typing import TypedDict
from car.instruction_controlled_car import (
    CarControlInstructions,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)

from car.model import CarModelSpecification
from car.turn_signals import TurnSignalType
from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_system.road_control_center.intersection_control_center.intersection_manoeuvre import (
    IntersectionManoeuvre,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection_control_center.schemas import (
    IntersectionCarManoeuvreInfo,
)

from traffic_control_system.road_control_center.car_simulation import CarSimulation
from traffic_control_system.schemas import IntersectionManoeuvreDescription, LiveCarData

MAX_DISTANCE_TO_POTENTIAL_MANOEUVRE_TRACK = 30


class CarOnIntersectionSimulation(TypedDict):
    car_simulation: CarSimulation
    manoeuvre: IntersectionManoeuvre


class IntersectionControlCenterSoftware:
    def __init__(
        self, intersection: Intersection, intersection_rules: IntersectionRules
    ):
        self.intersection = intersection
        self.intersection_rules = intersection_rules
        self.car_models_tracks: dict[
            str, dict[CardinalDirection, dict[CardinalDirection, IntersectionManoeuvre]]
        ] = {}

    def add_car_model_tracks(
        self,
        car_model_specification: CarModelSpecification,
    ) -> None:
        model_tracks: dict[
            CardinalDirection, dict[CardinalDirection, IntersectionManoeuvre]
        ] = {}
        for starting_side in CardinalDirection:
            starting_side_tracks: dict[CardinalDirection, IntersectionManoeuvre] = {}
            for ending_side in CardinalDirection:
                if starting_side == ending_side:
                    continue
                manoeuvre = IntersectionManoeuvre(
                    car_model_specification,
                    self.intersection,
                    {"starting_side": starting_side, "ending_side": ending_side},
                )
                starting_side_tracks[ending_side] = manoeuvre
            model_tracks[starting_side] = starting_side_tracks
        self.car_models_tracks[car_model_specification["name"]] = model_tracks

    def get_default_movement_instruction(self) -> CarControlInstructions:
        return {
            "movement_instructions": {
                "speed_instruction": SpeedInstruction.NO_CHANGE,
                "turn_instruction": TurnInstruction.NO_CHANGE,
            },
            "turn_signals_instruction": TurnSignalsInstruction.NO_SIGNALS_ON,
        }

    def approach_intersection_movement_instruction(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
    ) -> CarControlInstructions:
        live_car_data = live_cars_data[registry_number]
        manoeuvre = cars_manoeuvre_info[registry_number]["manoeuvre"]
        all_car_control_instructions = manoeuvre.get_all_car_control_instructions(
            live_car_data
        )
        for car_control_instructions in all_car_control_instructions[:-1]:
            if self.is_approaching_instruction_safe(
                registry_number,
                live_cars_data,
                car_control_instructions,
                cars_manoeuvre_info,
            ):
                return car_control_instructions
        return all_car_control_instructions[-1]

    def is_approaching_instruction_safe(
        self,
        registry_number: str,
        live_cars_data: dict[str, LiveCarData],
        car_control_instructions: CarControlInstructions,
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
    ) -> bool:
        live_car_data = live_cars_data[registry_number]
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        if manoeuvre_info["manoeuvre"].can_stop_before_zone(
            live_car_data,
            self.intersection.components["intersection_area"],
            car_control_instructions=car_control_instructions,
        ):
            return True
        can_safely_cross_the_intersection = self.can_safely_cross_the_intersection(
            registry_number,
            live_cars_data,
            car_control_instructions,
            cars_manoeuvre_info,
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
    ) -> bool:
        manoeuvre_info = cars_manoeuvre_info[registry_number]
        live_car_data = live_cars_data[registry_number]
        entering_intersection_status = manoeuvre_info[
            "manoeuvre"
        ].get_status_before_entering_zone(
            live_car_data,
            self.intersection.components["intersection_area"],
            car_control_instructions=car_control_instructions,
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
            },
            entering_intersection_status["time_to_enter_zone"],
        ):
            return False

        cars_with_priority = self.get_cars_with_priority(
            registry_number,
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
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
    ) -> list[str]:
        return [
            _registry_number
            for _registry_number in cars_manoeuvre_info
            if self.must_yield_the_right_of_way(
                registry_number,
                _registry_number,
                live_cars_data,
                cars_manoeuvre_info,
            )
        ]

    def must_yield_the_right_of_way(
        self,
        registry_number1: str,
        registry_number2: str,
        live_cars_data: dict[str, LiveCarData],
        cars_manoeuvre_info: dict[str, IntersectionCarManoeuvreInfo],
    ) -> bool:
        if registry_number1 == registry_number2:
            return False
        car2_possible_manoeuvres = self.get_currently_possible_manoeuvres(
            live_cars_data[registry_number2],
            cars_manoeuvre_info[registry_number2]["manoeuvre"].manoeuvre_description,
        )
        return any(
            [
                self.intersection_rules.must_yield_the_right_of_way(
                    {
                        "high_priority": live_cars_data[registry_number1]["live_state"][
                            "high_priority"
                        ],
                        "manoeuvre_description": cars_manoeuvre_info[registry_number1][
                            "manoeuvre"
                        ].manoeuvre_description,
                        "velocity": live_cars_data[registry_number1]["live_state"][
                            "velocity"
                        ],
                    },
                    {
                        "high_priority": live_cars_data[registry_number2]["live_state"][
                            "high_priority"
                        ],
                        "manoeuvre_description": car2_possible_manoeuvre,
                        "velocity": live_cars_data[registry_number2]["live_state"][
                            "velocity"
                        ],
                    },
                )
                for car2_possible_manoeuvre in car2_possible_manoeuvres
            ]
        )

    def get_currently_possible_manoeuvres(
        self,
        live_car_data: LiveCarData,
        manoeuvre_description: IntersectionManoeuvreDescription,
    ) -> list[IntersectionManoeuvreDescription]:
        starting_side = manoeuvre_description["starting_side"]
        if live_car_data["live_state"]["turn_signal"] != TurnSignalType.NO_SIGNAL:
            return [manoeuvre_description]
        result: list[IntersectionManoeuvreDescription] = []
        axle_center = CarSimulation.from_live_car_data(live_car_data).axle_center
        for ending_side in CardinalDirection:
            if ending_side == starting_side:
                continue
            manoeuvre = self.car_models_tracks[
                live_car_data["specification"]["model"]["name"]
            ][starting_side][ending_side]
            if (
                manoeuvre.track.get_distance_to_point(axle_center)
                < MAX_DISTANCE_TO_POTENTIAL_MANOEUVRE_TRACK
            ):
                result.append(
                    {"starting_side": starting_side, "ending_side": ending_side}
                )
        return result

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
        priority_cars: list[CarOnIntersectionSimulation] = []
        for _registry_number in cars_with_priority:
            priority_cars.extend(
                [
                    {
                        "car_simulation": CarSimulation.from_live_car_data(
                            live_cars_data[_registry_number]
                        ),
                        "manoeuvre": self.car_models_tracks[
                            live_cars_data[_registry_number]["specification"]["model"][
                                "name"
                            ]
                        ][manoeuvre_description["starting_side"]][
                            manoeuvre_description["ending_side"]
                        ],
                    }
                    for manoeuvre_description in self.get_currently_possible_manoeuvres(
                        live_cars_data[_registry_number],
                        cars_manoeuvre_info[_registry_number][
                            "manoeuvre"
                        ].manoeuvre_description,
                    )
                ]
            )
        car_simulation: CarOnIntersectionSimulation = {
            "car_simulation": CarSimulation.from_live_car_data(
                live_cars_data[registry_number]
            ),
            "manoeuvre": cars_manoeuvre_info[registry_number]["manoeuvre"],
        }
        car_simulation["car_simulation"].move(
            car_control_instructions["movement_instructions"]
        )
        for car in priority_cars:
            self._move_car_simulation(car)
        while not self.has_car_crossed_intersection(car_simulation):
            if self._priority_violation(
                car_simulation,
                priority_cars,
            ):
                return False
            for car in [*priority_cars, car_simulation]:
                self._move_car_simulation(car)
        return True

    def has_car_crossed_intersection(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ) -> bool:
        car_simulation = intersection_car_simulation["car_simulation"]
        manoeuvre_description = intersection_car_simulation[
            "manoeuvre"
        ].manoeuvre_description
        intersection_area = self.intersection.components["intersection_area"]
        outcoming_lane = self.intersection.components["outcoming_lanes"][
            manoeuvre_description["ending_side"]
        ]
        return not car_simulation.body_safe_zone.collides(
            intersection_area
        ) and car_simulation.collides(outcoming_lane)

    def _move_car_simulation(
        self,
        intersection_car_simulation: CarOnIntersectionSimulation,
    ) -> None:
        manoeuvre = intersection_car_simulation["manoeuvre"]
        car_simulation = intersection_car_simulation["car_simulation"]
        car_control_instructions = manoeuvre.get_car_control_instructions(
            car_simulation.get_live_data()
        )
        car_simulation.move(car_control_instructions["movement_instructions"])

    def _priority_violation(
        self,
        car: CarOnIntersectionSimulation,
        priority_cars: list[CarOnIntersectionSimulation],
    ) -> bool:
        return any(
            car_["car_simulation"].collides(car["car_simulation"].body_safe_zone)
            for car_ in priority_cars
        )
