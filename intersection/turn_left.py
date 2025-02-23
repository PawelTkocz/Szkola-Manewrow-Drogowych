from geometry import Directions
from intersection.animation import IntersectionAnimation
from intersection.priority_to_the_right_intersection import (
    PriorityToTheRightIntersection,
)
from state import State


class IntersectionTurnLeftAnimation(IntersectionAnimation):
    intersection = PriorityToTheRightIntersection()
    manoeuvre_directory_name = "turn_left"

    def __init__(self, previous_state: State, read_from_file: bool):
        super().__init__(
            previous_state,
            self.intersection,
            self.manoeuvre_directory_name,
            read_from_file,
        )
        self.add_car("red", Directions.RIGHT, Directions.UP, 0)
        self.add_car("blue", Directions.DOWN, Directions.UP, 0)
        self.add_car("brown", Directions.LEFT, Directions.UP, 0)
