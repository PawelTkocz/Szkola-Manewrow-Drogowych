import pygame

from Constants import OPTIONS_SCREENSHOT_SIZE
from State import State


class OptionToChoose:
    def __init__(
        self,
        title,
        image_path,
        on_click_state: State,
        *,
        image_width=OPTIONS_SCREENSHOT_SIZE,
        image_height=OPTIONS_SCREENSHOT_SIZE
    ):
        self.title = title
        self.image = pygame.transform.scale(
            self._load_image(image_path, image_width, image_height),
            (image_width, image_height),
        )
        self.on_click_state = on_click_state

    def _load_image(self, image_path, image_width, image_height):
        try:
            return pygame.image.load(image_path)
        except FileNotFoundError:
            return pygame.Surface((image_width, image_height))

    def on_click(self) -> State:
        return self.on_click_state
