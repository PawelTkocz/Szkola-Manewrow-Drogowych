from animations.animations_generators.intersection.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from application_screen import ApplicationScreen
from schemas import CardinalDirection
from smart_city.road_control_center.intersection.intersection_A0 import (
    intersection_A0_control_center,
)


class IntersectionTurnRightAnimation(IntersectionManoeuvreAnimation):
    manoeuvre_movement_instructions_dir = "turn_right"

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
                "starting_side": CardinalDirection.LEFT,
                "ending_side": CardinalDirection.DOWN,
            },
            0,
        )
        self.add_car(
            "DW002",
            "yellow",
            {
                "starting_side": CardinalDirection.RIGHT,
                "ending_side": CardinalDirection.UP,
            },
            0,
        )
        self.add_car(
            "DW003",
            "green",
            {
                "starting_side": CardinalDirection.UP,
                "ending_side": CardinalDirection.DOWN,
            },
            0,
        )
        self.add_car(
            "DW004",
            "orange",
            {
                "starting_side": CardinalDirection.DOWN,
                "ending_side": CardinalDirection.LEFT,
            },
            0,
        )
