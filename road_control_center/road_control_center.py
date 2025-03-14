from abc import ABC, abstractmethod

from car.autonomous_car import CarDataTransmitter


class RoadControlCenter(ABC):
    def __init__(self):
        self._time = 0

    def update_time(self):
        self._time += 1

    @abstractmethod
    def add_car(self, car_data_transmitter: CarDataTransmitter):
        pass

    @abstractmethod
    def remove_car(self, car_registry_number: str):
        pass

    @abstractmethod
    def send_movement_instructions(self) -> None:
        """Movement instruction for each registry number in cars_data"""
        pass
