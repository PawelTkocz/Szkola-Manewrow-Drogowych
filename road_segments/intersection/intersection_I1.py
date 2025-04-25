from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_signs.signs import SignA7, SignD1
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign


class IntersectionI1(Intersection):
    def __init__(self) -> None:
        signs: dict[CardinalDirection, list[TrafficSign]] = {
            CardinalDirection.DOWN: [SignA7()],
            CardinalDirection.LEFT: [SignD1()],
            CardinalDirection.RIGHT: [SignD1()],
            CardinalDirection.UP: [SignA7()],
        }
        super().__init__(traffic_signs=signs)
