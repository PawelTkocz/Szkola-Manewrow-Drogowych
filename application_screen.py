from abc import ABC, abstractmethod
from typing import Union

from pygame import Surface

from geometry import Point


class ApplicationScreen(ABC):
    @abstractmethod
    def render_frame(self, screen: Surface) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_click(
        self, mouse_click_point: Point
    ) -> Union["ApplicationScreen", None]:
        raise NotImplementedError
