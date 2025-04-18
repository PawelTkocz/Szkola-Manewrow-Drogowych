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
    PlaybackAnimationCarDescription,
)
from car.car import Car
from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)


class PlaybackAnimationCarInfo(TypedDict):
    car: InstructionControlledCar
    control_instructions: list[CarControlInstructions]
    start_frame_number: int


class PlaybackAnimation(AnimationStrategy):
    def __init__(
        self,
        cars_descriptions: Sequence[PlaybackAnimationCarDescription],
        control_instructions_dir_path: str,
    ) -> None:
        self.control_instructions_dir_path = control_instructions_dir_path
        self.cars: list[PlaybackAnimationCarInfo] = [
            {
                "car": self._generate_car(car_description),
                "start_frame_number": car_description["start_frame_number"],
                "control_instructions": self._load_control_instructions(
                    car_description["registry_number"]
                ),
            }
            for car_description in cars_descriptions
        ]
        self.frame_number = 0

    def _generate_car(
        self, car_description: PlaybackAnimationCarDescription
    ) -> InstructionControlledCar:
        return InstructionControlledCar(
            car_description["registry_number"],
            car_description["model"],
            car_description["starting_position"]["front_middle"],
            car_description["starting_position"]["direction"],
            car_description["velocity"],
            car_description["starting_position"]["wheels_direction"],
            color=car_description["color"],
        )

    def move_cars(self) -> list[Car]:
        for car in self.cars:
            if self.frame_number < car["start_frame_number"]:
                continue
            control_instructions_index = self.frame_number - car["start_frame_number"]
            if control_instructions_index >= len(car["control_instructions"]):
                continue
            control_instructions = car["control_instructions"][
                control_instructions_index
            ]
            car["car"].apply_control_instructions(control_instructions)
            car["car"].tick()
        self.frame_number += 1
        return [car["car"] for car in self.cars]

    def _load_control_instructions(
        self, registry_number: str
    ) -> list[CarControlInstructions]:
        file_path = os.path.join(
            self.control_instructions_dir_path,
            f"car_{registry_number}.json",
        )
        with open(file_path, "r") as file:
            control_instructions: list[CarControlInstructionsJSON] = json.load(file)
            return [
                {
                    "movement_instructions": {
                        "speed_instruction": SpeedInstruction(
                            control_instruction["speed_instruction"]
                        ),
                        "turn_instruction": TurnInstruction(
                            control_instruction["turn_instruction"]
                        ),
                    },
                    "turn_signals_instruction": TurnSignalsInstruction(
                        control_instruction["turn_signals_instruction"]
                    ),
                }
                for control_instruction in control_instructions
            ]

    def handle_quit(self) -> None:
        return
