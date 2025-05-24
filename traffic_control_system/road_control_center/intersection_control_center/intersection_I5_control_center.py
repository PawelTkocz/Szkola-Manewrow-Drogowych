from road_segments.intersection.intersection_I5 import IntersectionI5
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center import (
    IntersectionControlCenter,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_traffic_lights_rules import (
    IntersectionTrafficLightsRules,
)

INTERSECTION_RULES = IntersectionTrafficLightsRules()


class IntersectionI5ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI5(), INTERSECTION_RULES, "Intersection_I5")
