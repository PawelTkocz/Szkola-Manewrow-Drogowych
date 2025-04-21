from abc import ABC, abstractmethod

from pygame import Surface


class Drawable(ABC):
    @abstractmethod
    def draw(
        self,
        screen: Surface,
        *,
        scale_factor: float = 1,
        screen_y_offset: int = 0,
    ) -> None:
        raise NotImplementedError
