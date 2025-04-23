from abc import ABC, abstractmethod

from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModelSpecification
from smart_city.schemas import LiveCarData


class RoadCarController(ABC):
    @abstractmethod
    def register_new_active_car(self, live_car_data: LiveCarData) -> None:
        raise NotImplementedError

    @abstractmethod
    def calculate_control_instructions(
        self, registry_number: str
    ) -> CarControlInstructions:
        raise NotImplementedError

    @abstractmethod
    def update_active_cars_on_road(self, registry_numbers: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_car_model(
        self, car_model_specification: CarModelSpecification
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def register_tracks(self) -> bool:
        raise NotImplementedError
