from road_segments.intersection.intersection_I4 import IntersectionI4
from traffic_control_system.road_control_center.intersection_control_center.intersection_control_center import (
    IntersectionControlCenter,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_traffic_lights_rules import (
    IntersectionTrafficLightsRules,
)


class IntersectionI4ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        intersection = IntersectionI4()
        rules = IntersectionTrafficLightsRules(intersection.traffic_lights)
        super().__init__(intersection, rules, "Intersection_I4")
