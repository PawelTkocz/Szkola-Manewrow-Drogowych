from schemas import CardinalDirection
from traffic_control_system.road_control_center.intersection_control_center.minor_road_rule import (
    MinorRoadDescription,
    MinorRoadRule,
)
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSignName


class IntersectionI2Rules(MinorRoadRule):
    def __init__(self) -> None:
        minor_road1: MinorRoadDescription = {
            "side": CardinalDirection.LEFT,
            "sign": TrafficSignName.B20,
        }
        minor_road2: MinorRoadDescription = {
            "side": CardinalDirection.RIGHT,
            "sign": TrafficSignName.B20,
        }
        super().__init__(minor_road1, minor_road2)
