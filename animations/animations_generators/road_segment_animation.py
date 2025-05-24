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
from animations.animations_generators.constants import (
    BACKGROUND_COLOR,
    PLAYBACK_ANIMATIONS,
)
from animations.animations_generators.schemas import (
    AnimationCarDescription,
)
from animations.previous_screen_button import PreviousScreenButton
from application_screen import ApplicationScreen
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from screen_manager import get_screen
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.traffic_control_center import TrafficControlCenter


class RoadSegmentAnimation(ApplicationScreen):
    def __init__(
        self,
        cars_descriptions: list[AnimationCarDescription],
        control_instructions_dir_path: str,
        road_control_center: RoadControlCenter,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        self.previous_screen_button = (
            PreviousScreenButton(previous_app_screen) if previous_app_screen else None
        )
        self.traffic_control_center = TrafficControlCenter(road_control_center)
        self.animation_strategy: AnimationStrategy = (
            PlaybackAnimation(cars_descriptions, control_instructions_dir_path)
            if PLAYBACK_ANIMATIONS
            else RuntimeAnimation(
                cars_descriptions,
                control_instructions_dir_path,
                self.traffic_control_center,
            )
        )
        self.road_segment = road_control_center.road_segment
        self._register_car_models(cars_descriptions)
        self.road_elements_drafter = RoadElementsDrafter(
            self.road_segment.area, get_screen()
        )

    def _register_car_models(
        self, cars_descriptions: list[AnimationCarDescription]
    ) -> None:
        registered_models = set()
        for car_description in cars_descriptions:
            model = car_description["model"]
            name = model["name"]
            if name not in registered_models:
                self.traffic_control_center.register_car_model(model)
                registered_models.add(name)

    def render_frame(self, screen: Surface) -> None:
        self.traffic_control_center.tick()
        cars = self.animation_strategy.move_cars()
        screen.fill(BACKGROUND_COLOR)
        self.road_segment.draw(self.road_elements_drafter)
        for car in cars:
            car.draw(self.road_elements_drafter)
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
