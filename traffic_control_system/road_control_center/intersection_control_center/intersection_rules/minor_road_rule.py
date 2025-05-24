from typing import TypedDict
from schemas import CardinalDirection
from traffic_control_system.road_control_center.intersection_control_center.intersection_rules.intersection_rules import (
    IntersectionRules,
)
from traffic_control_system.road_control_center.intersection_control_center.schemas import (
    IntersectionPriorityCarInfo,
)
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSignName


class MinorRoadDescription(TypedDict):
    side: CardinalDirection
    sign: TrafficSignName


class MinorRoadRule(IntersectionRules):
    def __init__(
        self, minor_road1: MinorRoadDescription, minor_road2: MinorRoadDescription
    ) -> None:
        if minor_road1["side"] == minor_road2["side"]:
            raise ValueError("Intersection must define two different minor roads.")
        self.minor_roads = {
            minor_road1["side"]: minor_road1["sign"],
            minor_road2["side"]: minor_road2["sign"],
        }
        self.major_roads = {
            side for side in CardinalDirection if side not in self.minor_roads
        }

    def can_enter_intersection(
        self, car_info: IntersectionPriorityCarInfo, time_until_entry: int
    ) -> bool:
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        if (
            starting_side in self.minor_roads
            and self.minor_roads[starting_side] == TrafficSignName.B20
            and car_info["velocity"] != 0
        ):
            return False
        return True

    def is_on_road_with_priority(self, car_info: IntersectionPriorityCarInfo) -> bool:
        return car_info["manoeuvre_description"]["starting_side"] in self.major_roads
