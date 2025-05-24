from traffic_control_system.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection.schemas import (
    IntersectionPriorityCarInfo,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class IntersectionTrafficLightsRules(IntersectionRules):
    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        current_lights_state = car_info["traffic_lights_state"]["current"][
            starting_side
        ]
        if (
            current_lights_state
            in [TrafficLightsState.RED, TrafficLightsState.RED_YELLOW]
            or current_lights_state == TrafficLightsState.RED_WITH_ARROW
            and car_info["velocity"] != 0
        ):
            return False
        if current_lights_state == TrafficLightsState.GREEN:
            return True
        if (
            current_lights_state == TrafficLightsState.YELLOW
            and car_info["traffic_lights_state"]["entering_intersection_moment"][
                starting_side
            ]
            == TrafficLightsState.YELLOW
        ):
            return True
        return False

    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        lights_state = car_info["traffic_lights_state"]["current"][starting_side]
        if lights_state in [TrafficLightsState.GREEN, TrafficLightsState.YELLOW]:
            return True
        else:
            return False
