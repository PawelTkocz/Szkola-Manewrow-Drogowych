import os

from pygame import Surface
from animations.animations_generators.manoeuvre_animation import RoadSegmentAnimation
from animations.animations_generators.schemas import CarStartingPosition
from drafter.intersection import IntersectionDrafter
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)
from state import State
from animations.animations_generators.constants import (
    MOVEMENT_INSTRUCTIONS_DIR as movement_instructions_dir,
)
from animations.animations_generators.intersection.constants import (
    MOVEMENT_INSTRUCTIONS_DIR as intersection_movement_instructions_dir,
)


class IntersectionManoeuvreAnimation(RoadSegmentAnimation):
    def __init__(
        self,
        previous_state: State,
        manoeuvre_movement_instructions_dir: str,
        intersection_control_center: IntersectionControlCenter,
    ):
        movement_instructions_dir_path = os.path.join(
            movement_instructions_dir,
            intersection_movement_instructions_dir,
            manoeuvre_movement_instructions_dir,
        )
        super().__init__(
            previous_state,
            movement_instructions_dir_path,
            intersection_control_center,
        )
        self.intersection = intersection_control_center.intersection
        self.intersection_drafter = IntersectionDrafter(
            self.intersection.intersection_parts, self.intersection.intersection_colors
        )

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

    def draw_road(self, screen: Surface) -> None:
        self.intersection_drafter.draw(screen)
