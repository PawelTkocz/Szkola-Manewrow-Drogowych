from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_signs.signs import SignA5
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign


class IntersectionI0(Intersection):
    def __init__(self) -> None:
        signs: dict[CardinalDirection, list[TrafficSign]] = {
            direction: [SignA5()] for direction in CardinalDirection
        }
        super().__init__(traffic_signs=signs)
