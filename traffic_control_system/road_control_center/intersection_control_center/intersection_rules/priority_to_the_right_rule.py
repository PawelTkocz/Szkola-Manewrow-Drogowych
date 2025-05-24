from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection_control_center.schemas import (
    IntersectionPriorityCarInfo,
)


class PriorityToTheRightRule(IntersectionRules):
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        return True

    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        return False
