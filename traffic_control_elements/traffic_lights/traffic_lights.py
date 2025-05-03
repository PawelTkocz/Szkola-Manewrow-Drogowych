import pygame
from animations.constants import IMAGES_DIR_PATH
from geometry.direction import Direction
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
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

    def draw_on_road(self, road_elements_drafter: RoadElementsDrafter) -> None:
        road_elements_drafter.blit_surface(
            self.rotated_states_images[self.current_state], self._image_top_left
        )
