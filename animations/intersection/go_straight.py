from geometry import Directions
from intersection.animation import IntersectionAnimation
from intersection.priority_to_the_right_intersection import (
    PriorityToTheRightIntersection,
)
from state import State


class IntersectionGoStraightAnimation(IntersectionAnimation):
    intersection = PriorityToTheRightIntersection()
    manoeuvre_directory_name = "go_straight"

    def __init__(self, previous_state: State, read_from_file: bool):
        super().__init__(
            previous_state,
            self.intersection,
            self.manoeuvre_directory_name,
            read_from_file,
        )
        self.add_car("red", Directions.DOWN, Directions.RIGHT, 0)
        self.add_car("pink", Directions.LEFT, Directions.RIGHT, 0)
        self.add_car("purple", Directions.RIGHT, Directions.DOWN, 0)
