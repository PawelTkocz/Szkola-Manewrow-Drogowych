import os
from animations.animation_strategy import AnimationStrategy
from animations.schemas import CarStartingPosition, PlaybackAnimationCarInfo
from car.car import Car
from car.instruction_controlled_car import InstructionControlledCar
from car.toyota_yaris import ToyotaYaris
from geometry import Directions
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
from constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as general_car_movement_directory,
)
from animations.intersection.constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as intersection_car_movement_directory,
)
from traffic_control_center_software.schemas import SpeedModifications


class PlaybackAnimation(AnimationStrategy):
    def __init__(self, manoeuvre_directory_name: str):
        super().__init__(manoeuvre_directory_name)
        self.cars: list[PlaybackAnimationCarInfo] = []

    def add_car(
        self,
        registry_number: str,
        color: str,
        starting_position: CarStartingPosition,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ):
        car = InstructionControlledCar(
            registry_number,
            ToyotaYaris(),
            color,
            starting_position["front_middle"],
            starting_position["direction"],
        )
        movement_history = self._load_saved_car_movement(registry_number)
        self.cars.append(
            {
                "car": car,
                "movement_history": movement_history,
                "start_frame_number": start_frame_number,
            }
        )

    def move_cars(self, frame_number: int) -> list[Car]:
        for car_info in self.cars:
            if frame_number < car_info["start_frame_number"]:
                continue
            saved_movement_decision_index = (
                frame_number - car_info["start_frame_number"]
            )
            if saved_movement_decision_index >= len(car_info["movement_history"]):
                continue
            turn_direction, speed_modification = car_info["movement_history"][
                saved_movement_decision_index
            ]
            car_info["car"].move(
                movement_decision={
                    "speed_modification": SpeedModifications[speed_modification],
                    "turn_direction": Directions[turn_direction],
                }
            )
        return [car["car"] for car in self.cars]

    def _load_saved_car_movement(self, registry_number: str):
        file_path = os.path.join(
            general_car_movement_directory,
            intersection_car_movement_directory,
            self.manoeuvre_directory_name,
            f"car{registry_number}.txt",
        )
        with open(file_path, "r") as file:
            return [tuple(line.split()) for line in file]

    def handle_quit(self) -> None:
        return
