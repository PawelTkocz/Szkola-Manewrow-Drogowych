import json
import os
from typing import Sequence, TypedDict

from animations.animations_generators.animations_strategies.animation_strategy import (
    AnimationStrategy,
)
from animations.animations_generators.animations_strategies.schemas import (
    CarControlInstructionsJSON,
)
from animations.animations_generators.schemas import (
    AnimationCarDescription,
)
from car.car import Car
from car.instruction_controlled_car import CarControlInstructions

from smart_city.smart_city_car import SmartCityCar
from smart_city.traffic_control_center import (
    TrafficControlCenter,
)


class RuntimeAnimationCarInfo(TypedDict):
    car: SmartCityCar
    start_frame_number: int


class RuntimeAnimation(AnimationStrategy):
    def __init__(
        self,
        cars_descriptions: Sequence[AnimationCarDescription],
        control_instructions_dir_path: str,
        traffic_control_center: TrafficControlCenter,
    ) -> None:
        self.control_instructions_dir_path = control_instructions_dir_path
        self.traffic_control_center = traffic_control_center
        self.cars: list[RuntimeAnimationCarInfo] = [
            {
                "car": self._generate_car(car_description),
                "start_frame_number": car_description["start_frame_number"],
            }
            for car_description in cars_descriptions
        ]
        self.frame_number = 0

    def _generate_car(self, car_description: AnimationCarDescription) -> SmartCityCar:
        smart_city_car = SmartCityCar(
            car_description["registry_number"],
            car_description["model"],
            car_description["starting_position"]["front_middle"],
            car_description["starting_position"]["direction"],
            car_description["velocity"],
            car_description["starting_position"]["wheels_angle"],
            color=car_description["color"],
        )
        smart_city_car.set_manoeuvre(car_description["manoeuvre_description"])
        return smart_city_car

    def move_cars(self) -> list[Car]:
        for car in self._get_cars_that_start_movement():
            car["car"].connect_to_traffic_control_center(self.traffic_control_center)
        for car in self.cars:
            if self.frame_number < car["start_frame_number"]:
                continue
            car["car"].tick()
        self.frame_number += 1
        return [car["car"] for car in self.cars]

    def _get_cars_that_start_movement(self) -> list[RuntimeAnimationCarInfo]:
        return [
            car for car in self.cars if car["start_frame_number"] == self.frame_number
        ]

    def _serialize_control_instructions(
        self, control_instructions: list[CarControlInstructions]
    ) -> list[CarControlInstructionsJSON]:
        return [
            {
                "speed_instruction": control_instruction["movement_instructions"][
                    "speed_instruction"
                ].value,
                "turn_instruction": control_instruction["movement_instructions"][
                    "turn_instruction"
                ].value,
                "turn_signals_instruction": control_instruction[
                    "turn_signals_instruction"
                ].value,
            }
            for control_instruction in control_instructions
        ]

    def _save_control_instructions(self) -> None:
        os.makedirs(self.control_instructions_dir_path, exist_ok=True)
        for car in self.cars:
            file_path = os.path.join(
                self.control_instructions_dir_path,
                f"car_{car['car'].registry_number}.json",
            )
            with open(file_path, "w") as file:
                json.dump(
                    self._serialize_control_instructions(
                        car["car"].control_instructions_history
                    ),
                    file,
                    indent=4,
                )

    def handle_quit(self) -> None:
        self._save_control_instructions()
