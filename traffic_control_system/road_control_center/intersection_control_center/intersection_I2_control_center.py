from road_segments.intersection.intersection_I2 import IntersectionI2
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center import (
    IntersectionControlCenter,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_I2_rules import (
    IntersectionI2Rules,
)

INTERSECTION_RULES = IntersectionI2Rules()


class IntersectionI2ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI2(), INTERSECTION_RULES, "Intersection_I2")
