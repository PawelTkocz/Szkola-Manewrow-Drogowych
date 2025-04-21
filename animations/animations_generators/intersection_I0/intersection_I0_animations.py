from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.intersection.intersection_A0 import (
    IntersectionI0ControlCenter,
)
from smart_city.traffic_control_center import TrafficControlCenter


class IntersectionI0Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            Intersection(),
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            TrafficControlCenter(IntersectionI0ControlCenter()),
            previous_app_screen=previous_app_screen,
        )
