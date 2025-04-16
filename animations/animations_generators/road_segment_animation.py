from pygame import Surface

from animations.animations_generators.animations_strategies.animation_strategy import (
    AnimationStrategy,
)
from animations.animations_generators.animations_strategies.playback_animation import (
    PlaybackAnimation,
)
from animations.animations_generators.animations_strategies.runtime_animation import (
    RuntimeAnimation,
)
from animations.animations_generators.constants import PLAYBACK_ANIMATIONS
from animations.animations_generators.schemas import (
    AnimationCarDescription,
)
from animations.components.previous_screen_button import PreviousScreenButton
from application_screen import ApplicationScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from geometry import Point
from road_segments.constants import ROAD_SEGMENT_SIDE
from road_segments.road_segment import RoadSegment
from smart_city.traffic_control_center import TrafficControlCenter


class RoadSegmentAnimation(ApplicationScreen):
    def __init__(
        self,
        road_segment: RoadSegment,
        cars_descriptions: list[AnimationCarDescription],
        control_instructions_dir_path: str,
        traffic_control_center: TrafficControlCenter,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        self.road_segment = road_segment
        self.previous_screen_button = (
            PreviousScreenButton(previous_app_screen) if previous_app_screen else None
        )
        self.animation_strategy: AnimationStrategy = (
            PlaybackAnimation(cars_descriptions, control_instructions_dir_path)
            if PLAYBACK_ANIMATIONS
            else RuntimeAnimation(
                cars_descriptions, control_instructions_dir_path, traffic_control_center
            )
        )
        self.scale_factor = SCREEN_WIDTH / ROAD_SEGMENT_SIDE
        self.screen_y_offset = int(
            (SCREEN_HEIGHT - ROAD_SEGMENT_SIDE * self.scale_factor) // 2
        )

    def render_frame(self, screen: Surface) -> None:
        cars = self.animation_strategy.move_cars()
        self.road_segment.draw(
            screen, scale_factor=self.scale_factor, screen_y_offset=self.screen_y_offset
        )
        for car in cars:
            car.draw(
                screen,
                scale_factor=self.scale_factor,
                screen_y_offset=self.screen_y_offset,
            )
        if self.previous_screen_button:
            self.previous_screen_button.render(screen)

    def handle_click(self, mouse_click_point: Point) -> ApplicationScreen:
        if not self.previous_screen_button:
            return self
        previous_screen_requested = self.previous_screen_button.handle_click(
            mouse_click_point
        )
        if previous_screen_requested:
            self.animation_strategy.handle_quit()
        return previous_screen_requested or self
