from __future__ import annotations
from abc import ABC, abstractmethod


from pygame import Surface

from geometry.vector import Point


class ApplicationScreen(ABC):
    @abstractmethod
    def render_frame(self, screen: Surface) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen:
        raise NotImplementedError
