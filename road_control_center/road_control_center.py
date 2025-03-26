from abc import ABC, abstractmethod

from car.instruction_controlled_car import MovementInstruction
from smart_city.schemas import LiveCarData
from traffic_control_center_software.car_movement_simulator import (
    get_predicted_live_car_data,
)


class RoadControlCenter(ABC):
    def __init__(self):
        self._time = 0
        self._live_cars_data: dict[str, LiveCarData] = {}
        self._predicted_live_cars_data: dict[str, LiveCarData] = {}

    def tick(self, current_time: int) -> None:
        self._time = current_time
        cars_that_left_the_road = [
            registry_number
            for registry_number in self._live_cars_data
            if registry_number not in self._predicted_live_cars_data
        ]
        self._live_cars_data = self._predicted_live_cars_data
        self._predicted_live_cars_data = {}
        self._handle_cars_that_left_the_road(cars_that_left_the_road)

    def send_movement_instruction(
        self, live_car_data: LiveCarData
    ) -> MovementInstruction:
        registry_number = live_car_data["registry_number"]
        if registry_number not in self._live_cars_data:
            self._add_new_car_on_road(live_car_data)
        self._live_cars_data[registry_number] = live_car_data
        movement_instruction = self._get_movement_instruction(registry_number)
        self._predicted_live_cars_data[registry_number] = get_predicted_live_car_data(
            live_car_data, movement_instruction
        )
        return movement_instruction

    @abstractmethod
    def _add_new_car_on_road(self, live_car_data: LiveCarData) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get_movement_instruction(self, registry_number: str) -> MovementInstruction:
        raise NotImplementedError

    @abstractmethod
    def _handle_cars_that_left_the_road(self, cars_registry_numbers: list[str]) -> None:
        raise NotImplementedError
