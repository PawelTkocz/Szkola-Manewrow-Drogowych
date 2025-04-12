import os

from pygame import Surface
from animations.animations_generators.manoeuvre_animation import RoadSegmentAnimation
from animations.animations_generators.schemas import CarStartingPosition
from application_screen import ApplicationScreen
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)
from animations.animations_generators.constants import (
    MOVEMENT_INSTRUCTIONS_DIR as movement_instructions_dir,
)
from animations.animations_generators.intersection.constants import (
    MOVEMENT_INSTRUCTIONS_DIR as intersection_movement_instructions_dir,
)


class IntersectionManoeuvreAnimation(RoadSegmentAnimation):
    def __init__(
        self,
        manoeuvre_movement_instructions_dir: str,
        intersection_control_center: IntersectionControlCenter,
        *,
        previous_app_screen: ApplicationScreen | None = None,
    ):
        movement_instructions_dir_path = os.path.join(
            movement_instructions_dir,
            intersection_movement_instructions_dir,
            manoeuvre_movement_instructions_dir,
        )
        super().__init__(
            movement_instructions_dir_path,
            intersection_control_center,
            previous_app_screen=previous_app_screen,
        )
        self.intersection = intersection_control_center.intersection

    def get_starting_position(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> CarStartingPosition:
        starting_side = manoeuvre_description["starting_side"]
        front_middle_position = self.intersection.intersection_parts["incoming_lines"][
            starting_side
        ].rear_middle
        direction = self.intersection.intersection_parts["incoming_lines"][
            starting_side
        ].direction
        return {"front_middle": front_middle_position, "direction": direction}

    def draw_road(
        self, screen: Surface, *, scale: float = 1, screen_y_offset: int = 0
    ) -> None:
        self.intersection.draw(screen, scale=scale, screen_y_offset=screen_y_offset)
