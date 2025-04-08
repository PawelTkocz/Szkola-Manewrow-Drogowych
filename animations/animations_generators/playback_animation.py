import os

from animations.animations_generators.animation_strategy import AnimationStrategy
from animations.animations_generators.schemas import (
    CarStartingPosition,
    PlaybackAnimationCarInfo,
)
from car.car import Car
from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
    SpeedInstruction,
    TurnInstruction,
    TurnSignalsInstruction,
)
from car.toyota_yaris import ToyotaYaris
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)


# think about not writing to txt but json
class PlaybackAnimation(AnimationStrategy):
    def __init__(self, movement_instructions_dir_path: str) -> None:
        super().__init__(movement_instructions_dir_path)
        self.cars: list[PlaybackAnimationCarInfo] = []

    def add_car(
        self,
        registry_number: str,
        color: str,
        starting_position: CarStartingPosition,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ) -> None:
        car = InstructionControlledCar(
            registry_number,
            ToyotaYaris(),
            color,
            starting_position["front_middle"],
            starting_position["direction"],
        )
        self.cars.append(
            {
                "car": car,
                "movement_instructions": self._load_movement_instructions(
                    registry_number
                ),
                "start_frame_number": start_frame_number,
            }
        )

    def move_cars(self, frame_number: int) -> list[Car]:
        for car in self.cars:
            if frame_number < car["start_frame_number"]:
                continue
            movement_instruction_index = frame_number - car["start_frame_number"]
            if movement_instruction_index >= len(car["movement_instructions"]):
                continue
            movement_instruction = car["movement_instructions"][
                movement_instruction_index
            ]
            car["car"].tick(movement_instruction)
        return [car["car"] for car in self.cars]

    def _load_movement_instructions(
        self, registry_number: str
    ) -> list[CarControlInstructions]:
        file_path = os.path.join(
            self.movement_instructions_dir_path,
            f"car_{registry_number}.txt",
        )
        with open(file_path, "r") as file:
            return [
                {
                    "movement_instructions": {
                        "speed_instruction": SpeedInstruction[speed_mod],
                        "turn_instruction": TurnInstruction[turn_mod],
                    },
                    "turn_signals_instruction": TurnSignalsInstruction[
                        turn_sig_instrcution
                    ],
                }
                for speed_mod, turn_mod, turn_sig_instrcution in (
                    line.split() for line in file
                )
            ]

    def handle_quit(self) -> None:
        return
