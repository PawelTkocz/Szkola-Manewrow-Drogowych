from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
    IntersectionPriorityCarInfo,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class IntersectionTrafficLightsRules(IntersectionRules):
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign)"""
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        lights_state = car_info["traffic_lights_state"][starting_side]
        if lights_state in [TrafficLightsState.GREEN, TrafficLightsState.YELLOW]:
            return True
        else:
            return False
        # add rule for conditional arrow

    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        lights_state = car_info["traffic_lights_state"][starting_side]
        if lights_state in [TrafficLightsState.GREEN, TrafficLightsState.YELLOW]:
            return True
        else:
            return False
