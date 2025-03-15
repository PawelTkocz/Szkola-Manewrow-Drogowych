from animations.manoeuvre_animation import ManoeuvreAnimation
from animations.schemas import CarStartingPosition
from drafter.intersection import IntersectionDrafter
from road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
from state import State


class IntersectionManoeuvreAnimation(ManoeuvreAnimation):
    def __init__(
        self,
        previous_state: State,
        manoeuvre_directory_name: str,
        intersection_control_center: IntersectionControlCenter,
    ):
        super().__init__(
            previous_state,
            manoeuvre_directory_name,
            intersection_control_center,
        )
        self.intersection = intersection_control_center.intersection
        self.intersection_drafter = IntersectionDrafter(
            self.intersection.intersection_parts
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

    def draw_road(self, screen):
        self.intersection_drafter.draw(screen)
