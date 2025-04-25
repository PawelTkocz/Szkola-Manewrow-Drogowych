from road_segments.intersection.intersection_I4 import IntersectionI4
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.intersection.intersection_traffic_lights_rules import (
    IntersectionTrafficLightsRules,
)

INTERSECTION_RULES = IntersectionTrafficLightsRules()


class IntersectionI4ControlCenter(IntersectionControlCenter):
    def __init__(self) -> None:
        super().__init__(IntersectionI4(), INTERSECTION_RULES, "Intersection_I4")
