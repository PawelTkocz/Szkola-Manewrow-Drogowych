from road_segments.intersection.intersection_A0 import IntersectionA0
from smart_city.road_control_center.intersection.intersection_control_center import (
    IntersectionControlCenter,
)
from smart_city.road_control_center.intersection.priority_to_the_right_rule import (
    PriorityToTheRightRule,
)

intersection_A0_control_center = IntersectionControlCenter(
    IntersectionA0(), PriorityToTheRightRule()
)
