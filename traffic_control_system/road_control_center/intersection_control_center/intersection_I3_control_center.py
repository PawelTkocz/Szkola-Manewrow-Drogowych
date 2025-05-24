from road_segments.intersection.intersection_I3 import IntersectionI3
from traffic_control_system.road_control_center.intersection_control_center.intersection_I3_rules import (
    IntersectionI3Rules,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center import (
    IntersectionControlCenter,
)

INTERSECTION_RULES = IntersectionI3Rules()


class IntersectionI3ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI3(), INTERSECTION_RULES, "Intersection_I3")
