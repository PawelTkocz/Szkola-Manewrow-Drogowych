from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from road_segments.intersection.intersection_I1 import IntersectionI1
from smart_city.road_control_center.intersection.intersection_I1_control_center import (
    IntersectionI1ControlCenter,
)


class IntersectionI1Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            IntersectionI1(),
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            IntersectionI1ControlCenter(),
            previous_app_screen=previous_app_screen,
        )
