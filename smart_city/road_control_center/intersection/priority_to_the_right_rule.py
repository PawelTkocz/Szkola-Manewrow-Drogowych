from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionPriorityCarInfo,
)


class PriorityToTheRightRule(IntersectionRules):
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign)"""
        # there are no stop signs, no traffic lights
        return True

    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        return False
