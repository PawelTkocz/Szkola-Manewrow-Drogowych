from road_segments.intersection.intersection_I1 import IntersectionI1
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center import (
    IntersectionControlCenter,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_I1_rules import (
    IntersectionI1Rules,
)

INTERSECTION_RULES = IntersectionI1Rules()


class IntersectionI1ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI1(), INTERSECTION_RULES, "Intersection_I1")
