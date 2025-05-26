from traffic_control_elements.traffic_lights.intersection.intersection_traffic_lights import (
    IntersectionTrafficLights,
)
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection_control_center.schemas import (
    IntersectionPriorityCarInfo,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState
from utils import clockwise_direction_shift


class IntersectionTrafficLightsRules(IntersectionRules):
    def __init__(self, traffic_lights: IntersectionTrafficLights) -> None:
        self.traffic_lights = traffic_lights

    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time_until_entry: int
    ) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        ending_side = car_info["manoeuvre_description"]["ending_side"]
        current_lights_state = self.traffic_lights.get_lights_states()[starting_side]

        if current_lights_state == TrafficLightsState.GREEN:
            return True
        if (
            current_lights_state == TrafficLightsState.YELLOW
            and self.traffic_lights.get_future_lights_states(time_until_entry)[
                starting_side
            ]
            == TrafficLightsState.YELLOW
        ):
            return True
        if (
            current_lights_state == TrafficLightsState.RED_WITH_ARROW
            and clockwise_direction_shift(starting_side, 3) == ending_side
            and car_info["velocity"] == 0
        ):
            return True
        return False

    def is_on_road_with_priority(self, car_info: IntersectionPriorityCarInfo) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        lights_state = self.traffic_lights.get_lights_states()[starting_side]
        return lights_state in [TrafficLightsState.GREEN, TrafficLightsState.YELLOW]
