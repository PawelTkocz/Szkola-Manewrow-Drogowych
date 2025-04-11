from animations.animations_generators.intersection.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from application_screen.application_screen import ApplicationScreen
from schemas import CardinalDirection
from smart_city.road_control_center.intersection.intersection_A0 import (
    intersection_A0_control_center,
)


class IntersectionGoStraightAnimation(IntersectionManoeuvreAnimation):
    manoeuvre_movement_instructions_dir = "go_straight"

    def __init__(self, previous_state: ApplicationScreen):
        super().__init__(
            previous_state,
            self.manoeuvre_movement_instructions_dir,
            intersection_A0_control_center,
        )
        self.add_car(
            "DW001",
            "red",
            {
                "starting_side": CardinalDirection.DOWN,
                "ending_side": CardinalDirection.RIGHT,
            },
            0,
        )
        self.add_car(
            "DW002",
            "pink",
            {
                "starting_side": CardinalDirection.LEFT,
                "ending_side": CardinalDirection.RIGHT,
            },
            0,
        )
        self.add_car(
            "DW003",
            "purple",
            {
                "starting_side": CardinalDirection.RIGHT,
                "ending_side": CardinalDirection.DOWN,
            },
            0,
        )
