from abc import abstractmethod

from pygame import Surface

from animations.animations_generators.animation_strategy import AnimationStrategy
from animations.animations_generators.constants import PLAYBACK_ANIMATIONS
from animations.animations_generators.playback_animation import PlaybackAnimation
from animations.animations_generators.runtime_animation import RuntimeAnimation
from animations.animations_generators.schemas import CarStartingPosition
from application_screen.application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from road_segments.constants import SEGMENT_SIDE
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.road_control_center import RoadControlCenter


class RoadSegmentAnimation(ApplicationScreen):
    def __init__(
        self,
        previous_state: ApplicationScreen,
        movement_instructions_dir_path: str,
        road_control_center: RoadControlCenter,
    ) -> None:
        self.previous_state = previous_state
        self.frame_number = 0
        self.animation_strategy: AnimationStrategy = (
            PlaybackAnimation(movement_instructions_dir_path)
            if PLAYBACK_ANIMATIONS
            else RuntimeAnimation(movement_instructions_dir_path, road_control_center)
        )
        self.scale = SCREEN_WIDTH / SEGMENT_SIDE
        self.screen_y_offset = int((SCREEN_HEIGHT - SEGMENT_SIDE * self.scale) // 2)

    @abstractmethod
    def get_starting_position(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> CarStartingPosition:
        pass

    @abstractmethod
    def draw_road(
        self, screen: Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        pass

    def add_car(
        self,
        registry_number: str,
        color: str,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ) -> None:
        starting_position = self.get_starting_position(manoeuvre_description)
        self.animation_strategy.add_car(
            registry_number,
            color,
            starting_position,
            manoeuvre_description,
            start_frame_number,
        )

    def render_frame(self, screen: Surface) -> None:
        cars = self.animation_strategy.move_cars(self.frame_number)
        self.draw_road(screen, scale=self.scale, screen_y_offset=self.screen_y_offset)
        for car in cars:
            car.draw(screen, scale=self.scale, screen_y_offset=self.screen_y_offset)
        self.frame_number += 1

    def handle_click(
        self, mouse_click_position: tuple[float, float]
    ) -> ApplicationScreen:
        return self.previous_state

    def handle_quit(self) -> None:
        self.animation_strategy.handle_quit()
