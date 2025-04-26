import pygame
from animations.constants import IMAGES_DIR_PATH
from drafter.utils import blit_surface
from geometry.direction import Direction
from geometry.vector import Point
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_lights.schemas import (
    TrafficLightsState,
)


class TrafficLights(TrafficControlElement):
    def __init__(
        self,
        states_images_file_names: dict[TrafficLightsState, str],
        width: float,
        height: float,
        start_state: TrafficLightsState,
    ) -> None:
        super().__init__(width, height)
        self.states_images = {
            state: pygame.transform.scale(
                pygame.image.load(
                    f"{IMAGES_DIR_PATH}/{states_images_file_names[state]}"
                ),
                (width, height),
            )
            for state in states_images_file_names
        }
        self.rotated_states_images = self.states_images.copy()
        self.current_state = start_state

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        super().update_position(front_middle, direction)
        for state in self.rotated_states_images:
            self.rotated_states_images[state] = pygame.transform.rotate(
                self.states_images[state], self.rotation_angle
            )

    def set_state(self, state: TrafficLightsState) -> None:
        self.current_state = state

    def get_state(self) -> TrafficLightsState:
        return self.current_state

    def draw(
        self, screen: pygame.Surface, *, scale_factor=1, screen_y_offset=0
    ) -> None:
        blit_surface(
            screen,
            self.rotated_states_images[self.current_state],
            self._image_top_left,
            scale_factor=scale_factor,
            screen_y_offset=screen_y_offset,
        )
