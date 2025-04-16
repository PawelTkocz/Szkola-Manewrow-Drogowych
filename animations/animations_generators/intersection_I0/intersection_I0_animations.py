from animations.animations_generators.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from animations.animations_generators.schemas import IntersectionAnimationCarDescription
from application_screen import ApplicationScreen
from road_segments.intersection.intersection_I0 import IntersectionI0
from smart_city.road_control_center.intersection.intersection_A0 import (
    IntersectionI0ControlCenter,
)
from smart_city.traffic_control_center import TrafficControlCenter

INTERSECTION = IntersectionI0()
TRAFFIC_CONTROL_CENTER = TrafficControlCenter(IntersectionI0ControlCenter())


class IntersectionI0Animation(IntersectionManoeuvreAnimation):
    def __init__(
        self,
        cars_descriptions: list[IntersectionAnimationCarDescription],
        manoeuvre_control_instructions_dir_name: str,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ) -> None:
        super().__init__(
            INTERSECTION,
            cars_descriptions,
            manoeuvre_control_instructions_dir_name,
            TRAFFIC_CONTROL_CENTER,
            previous_app_screen=previous_app_screen,
        )
