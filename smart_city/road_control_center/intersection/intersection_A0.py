from road_segments.intersection.intersection import Intersection
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.intersection.priority_to_the_right_rule import (
    PriorityToTheRightRule,
)

INTERSECTION = Intersection()
INTERSECTION_RULES = PriorityToTheRightRule()


class IntersectionI0ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(INTERSECTION, INTERSECTION_RULES, "Intersection_I0")
