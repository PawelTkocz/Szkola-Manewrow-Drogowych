from abc import ABC, abstractmethod
import pygame

from application_screen.application_screen import ApplicationScreen


class MenuOptionsPanel(ABC):
    @abstractmethod
    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> ApplicationScreen | None:
        raise NotImplementedError

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        raise NotImplementedError
