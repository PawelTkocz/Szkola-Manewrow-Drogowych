from abc import ABC, abstractmethod
from animations.animations_generators.schemas import CarStartingPosition
from car.car import Car
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)


class AnimationStrategy(ABC):
    def __init__(self, movement_instructions_dir_path: str):
        self.movement_instructions_dir_path = movement_instructions_dir_path

    @abstractmethod
    def add_car(
        self,
        registry_number: str,
        color: str,
        starting_position: CarStartingPosition,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ) -> None:
        pass

    @abstractmethod
    def move_cars(self, frame_number: int) -> list[Car]:
        pass

    @abstractmethod
    def handle_quit(self) -> None:
        pass
