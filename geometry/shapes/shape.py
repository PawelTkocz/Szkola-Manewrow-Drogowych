from abc import ABC, abstractmethod

from pygame import Surface


class Shape(ABC):
    @abstractmethod
    def draw(self, screen: Surface) -> None:
        raise NotImplementedError
