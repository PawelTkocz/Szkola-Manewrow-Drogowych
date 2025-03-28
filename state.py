from abc import ABC, abstractmethod

from pygame import Surface


class State(ABC):
    def __init__(self, *, previous_state: "State"):
        self.previous_state = previous_state

    @abstractmethod
    def render_frame(self, screen: Surface) -> None:
        pass

    @abstractmethod
    def handle_click(self, mouse_click_position: tuple[float, float]) -> "State":
        pass

    @abstractmethod
    def handle_quit(self) -> None:
        pass
