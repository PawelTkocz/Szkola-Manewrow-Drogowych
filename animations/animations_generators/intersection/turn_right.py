from animations.animations_generators.intersection.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from geometry import Directions
from state import State
from smart_city.road_control_center.intersection.intersection_A0 import (
    intersection_A0_control_center,
)


class IntersectionTurnRightAnimation(IntersectionManoeuvreAnimation):
    manoeuvre_movement_instructions_dir = "turn_right"

    def __init__(self, previous_state: State):
        super().__init__(
            previous_state,
            self.manoeuvre_movement_instructions_dir,
            intersection_A0_control_center,
        )
        self.add_car(
            "DW001",
            "red",
            {"starting_side": Directions.LEFT, "ending_side": Directions.DOWN},
            0,
        )
        self.add_car(
            "DW002",
            "yellow",
            {"starting_side": Directions.RIGHT, "ending_side": Directions.UP},
            0,
        )
        self.add_car(
            "DW003",
            "green",
            {"starting_side": Directions.UP, "ending_side": Directions.DOWN},
            0,
        )
        self.add_car(
            "DW004",
            "orange",
            {"starting_side": Directions.DOWN, "ending_side": Directions.LEFT},
            0,
        )
