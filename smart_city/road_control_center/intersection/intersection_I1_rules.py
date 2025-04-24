from schemas import CardinalDirection
from smart_city.road_control_center.intersection.minor_road_rule import (
    MinorRoadDescription,
    MinorRoadRule,
)
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSignName


class IntersectionI1Rules(MinorRoadRule):
    def __init__(self) -> None:
        minor_road1: MinorRoadDescription = {
            "side": CardinalDirection.UP,
            "sign": TrafficSignName.A7,
        }
        minor_road2: MinorRoadDescription = {
            "side": CardinalDirection.DOWN,
            "sign": TrafficSignName.A7,
        }
        super().__init__(minor_road1, minor_road2)
