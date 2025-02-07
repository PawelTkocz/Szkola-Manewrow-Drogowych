from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, *, previous_state: "State" = None):
        self.previous_state = previous_state

    @abstractmethod
    def render_frame(self, screen):
        pass

    @abstractmethod
    def handle_click(self, mouse_click_position) -> "State":
        pass

    @abstractmethod
    def handle_quit(self):
        pass
