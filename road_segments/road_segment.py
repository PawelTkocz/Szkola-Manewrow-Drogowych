from abc import ABC, abstractmethod

from pygame import Surface

from geometry.shapes.rectangle import AxisAlignedRectangle


class RoadSegment(ABC):
    @abstractmethod
    def draw(
        self, screen: Surface, *, scale_factor: float = 1, screen_y_offset: int = 0
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def tick(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def area(self) -> AxisAlignedRectangle:
        raise NotImplementedError
