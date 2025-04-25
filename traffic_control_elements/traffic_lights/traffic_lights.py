import pygame
from animations.constants import IMAGES_DIR_PATH
from drafter.utils import blit_surface
from geometry.direction import Direction
from geometry.vector import Point
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_lights.traffic_lights_coordinator import (
    TrafficLightsCoordinator,
    TrafficLightsState,
)

TRAFFIC_LIGHTS_WIDTH = 50


class TrafficLights(TrafficControlElement):
    def __init__(
        self,
        states_images_file_names: dict[TrafficLightsState, str],
        start_tick: int,
        traffic_lights_coordinator: TrafficLightsCoordinator,
    ) -> None:
        super().__init__(TRAFFIC_LIGHTS_WIDTH, TRAFFIC_LIGHTS_WIDTH)
        self.states_images = {
            state: pygame.transform.scale(
                pygame.image.load(
                    f"{IMAGES_DIR_PATH}/{states_images_file_names[state]}"
                ),
                (TRAFFIC_LIGHTS_WIDTH, TRAFFIC_LIGHTS_WIDTH),
            )
            for state in TrafficLightsState
        }
        self.rotated_states_images = self.states_images.copy()
        self.current_tick = start_tick
        self.traffic_lights_coordinator = traffic_lights_coordinator
        self.current_state = traffic_lights_coordinator.get_state(start_tick)

    def update_position(self, front_middle: Point, direction: Direction) -> None:
        super().update_position(front_middle, direction)
        for state in TrafficLightsState:
            self.rotated_states_images[state] = pygame.transform.rotate(
                self.states_images[state], self.rotation_angle
            )

    def tick(self) -> None:
        self.current_tick += 1
        self.current_state = self.traffic_lights_coordinator.get_state(
            self.current_tick
        )

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

    def get_state(self) -> TrafficLightsState:
        return self.current_state
