from abc import ABC, abstractmethod
from enum import Enum


class ConditionalArrowState(Enum):
    ON = "ON"
    OFF = "OFF"


class ConditionalArrowLightCoordinator(ABC):
    @abstractmethod
    def get_state(self, time: int) -> ConditionalArrowState:
        raise NotImplementedError
