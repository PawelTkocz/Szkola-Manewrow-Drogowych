from animations.intersection.intersection_manoeuvre_animation import (
    IntersectionManoeuvreAnimation,
)
from geometry import Directions
from road_control_center.intersection.intersection_A0 import IntersectionA0ControlCenter
from state import State


class IntersectionTurnLeftAnimation(IntersectionManoeuvreAnimation):
    intersection_control_center = IntersectionA0ControlCenter()
    manoeuvre_directory_name = "turn_left"

    def __init__(self, previous_state: State):
        super().__init__(
            previous_state,
            self.manoeuvre_directory_name,
            self.intersection_control_center,
        )
        self.add_car(
            "DW001",
            "red",
            {"starting_side": Directions.RIGHT, "ending_side": Directions.UP},
            0,
        )
        self.add_car(
            "DW002",
            "blue",
            {"starting_side": Directions.DOWN, "ending_side": Directions.UP},
            0,
        )
        self.add_car(
            "DW003",
            "brown",
            {"starting_side": Directions.LEFT, "ending_side": Directions.UP},
            0,
        )
