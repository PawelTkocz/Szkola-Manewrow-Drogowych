from road_segments.intersection.intersection_I1 import IntersectionI1
from smart_city.road_control_center.intersection.intersection_I1_rules import (
    IntersectionI1Rules,
)
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)

INTERSECTION_RULES = IntersectionI1Rules()


class IntersectionI1ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI1(), INTERSECTION_RULES, "Intersection_I1")
