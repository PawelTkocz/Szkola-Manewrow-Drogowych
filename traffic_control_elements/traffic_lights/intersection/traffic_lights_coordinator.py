from abc import ABC, abstractmethod

from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class IntersectionTrafficLightsCoordinator(ABC):
    @abstractmethod
    def get_states(
        self, tick_number: int
    ) -> dict[CardinalDirection, TrafficLightsState]:
        raise NotImplementedError
