from abc import ABC, abstractmethod
from enum import Enum


class TrafficLightsState(Enum):
    RED = "RED"
    RED_YELLOW = "RED_YELLOW"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class TrafficLightsCoordinator(ABC):
    @abstractmethod
    def get_state(self, time: int) -> TrafficLightsState:
        raise NotImplementedError
