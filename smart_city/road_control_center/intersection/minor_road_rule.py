from typing import TypedDict
from schemas import CardinalDirection
from smart_city.road_control_center.intersection.intersection_rules import (
    IntersectionRules,
)
from smart_city.road_control_center.intersection.schemas import (
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
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        """Determine if car can enter intersection (traffic lights, stop sign)"""
        # there are no stop signs, no traffic lights
        starting_side = car_info["manoeuvre_description"]["starting_side"]
        if (
            starting_side in self.minor_roads
            and self.minor_roads[starting_side] == TrafficSignName.B20
            and car_info["velocity"] != 0
        ):
            return False
        return True

    def is_on_road_with_priority(
        self, car_info: IntersectionPriorityCarInfo, time: int
    ) -> bool:
        return car_info["manoeuvre_description"]["starting_side"] in self.major_roads
