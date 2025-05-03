from pygame import Surface
from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from road_segments.intersection.intersection_I3 import IntersectionI3
from smart_city.road_control_center.intersection.intersection_I3_control_center import (
    IntersectionI3ControlCenter,
)


class IntersectionI3Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        screen: Surface,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            IntersectionI3(),
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            IntersectionI3ControlCenter(),
            screen,
            previous_app_screen=previous_app_screen,
        )
