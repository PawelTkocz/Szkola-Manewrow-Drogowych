from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from road_segments.intersection.intersection_I5 import IntersectionI5
from smart_city.road_control_center.intersection.intersection_I5_control_center import (
    IntersectionI5ControlCenter,
)


class IntersectionI5Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            IntersectionI5(),
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            IntersectionI5ControlCenter(),
            previous_app_screen=previous_app_screen,
        )
