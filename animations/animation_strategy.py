from abc import ABC, abstractmethod
from animations.schemas import CarStartingPosition
from car.car import Car
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription


class AnimationStrategy(ABC):
    def __init__(self, manoeuvre_directory_name: str):
        self.manoeuvre_directory_name = manoeuvre_directory_name

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
