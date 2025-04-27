from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_signs.signs import SignB20, SignD1
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign


class IntersectionI2(Intersection):
    def __init__(self) -> None:
        signs: dict[CardinalDirection, list[TrafficSign]] = {
            CardinalDirection.DOWN: [SignD1()],
            CardinalDirection.LEFT: [SignB20()],
            CardinalDirection.RIGHT: [SignB20()],
            CardinalDirection.UP: [SignD1()],
        }
        super().__init__(traffic_signs=signs)
