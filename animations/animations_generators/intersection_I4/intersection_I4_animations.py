from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from smart_city.road_control_center.intersection.intersection_I4_control_center import (
    IntersectionI4ControlCenter,
)


class IntersectionI4Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            IntersectionI4ControlCenter(),
            previous_app_screen=previous_app_screen,
        )
