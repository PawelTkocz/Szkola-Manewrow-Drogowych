from abc import ABC, abstractmethod

from geometry.shapes.rectangle import AxisAlignedRectangle
from road_elements_drafter import RoadElementsDrafter


class RoadSegment(ABC):
    @abstractmethod
    def draw(self, road_elements_drafter: RoadElementsDrafter) -> None:
        raise NotImplementedError

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def area(self) -> AxisAlignedRectangle:
        raise NotImplementedError
