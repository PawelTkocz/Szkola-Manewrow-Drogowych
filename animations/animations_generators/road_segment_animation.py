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
from geometry.vector import Point
from road_elements_drafter import RoadElementsDrafter
from road_segments.road_segment import RoadSegment
from screen_manager import get_screen
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.traffic_control_center import TrafficControlCenter


class RoadSegmentAnimation(ApplicationScreen):
    def __init__(
        self,
        road_segment: RoadSegment,
        cars_descriptions: list[AnimationCarDescription],
        control_instructions_dir_path: str,
        road_control_center: RoadControlCenter,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        self.road_segment = road_segment
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
        car_models = {
            car_description["model"]["name"] for car_description in cars_descriptions
        }
        for car_model in [
            car_description["model"] for car_description in cars_descriptions
        ]:
            if car_model["name"] in car_models:
                self.traffic_control_center.register_car_model(car_model)
                car_models.remove(car_model["name"])
        self.road_elements_drafter = RoadElementsDrafter(
            road_segment.area, get_screen()
        )

    def render_frame(self, screen: Surface) -> None:
        self.road_segment.tick()
        self.traffic_control_center.tick()
        cars = self.animation_strategy.move_cars()
        screen.fill("red")
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
