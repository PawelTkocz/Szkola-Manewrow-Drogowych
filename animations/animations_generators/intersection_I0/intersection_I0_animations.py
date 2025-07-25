from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from traffic_control_system.road_control_center.intersection_control_center.intersection_I0_control_center import (
    IntersectionI0ControlCenter,
)


class IntersectionI0Animation(IntersectionManoeuvreAnimation):
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
            IntersectionI0ControlCenter(),
            previous_app_screen=previous_app_screen,
        )
