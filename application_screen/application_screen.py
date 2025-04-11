from abc import ABC, abstractmethod

from pygame import Surface


class ApplicationScreen(ABC):
    @abstractmethod
    def render_frame(self, screen: Surface) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> "ApplicationScreen":
        raise NotImplementedError
