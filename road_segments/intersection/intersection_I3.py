from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_signs.signs import (
    SignA7,
    SignD1,
    SignT6aLeft,
    SignT6aRight,
    SignT6cLeft,
    SignT6cRight,
)
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign


class IntersectionI3(Intersection):
    def __init__(self) -> None:
        control_elements: dict[CardinalDirection, list[TrafficSign]] = {
            CardinalDirection.DOWN: [SignA7(), SignT6cRight()],
            CardinalDirection.LEFT: [SignD1(), SignT6aLeft()],
            CardinalDirection.RIGHT: [SignA7(), SignT6cLeft()],
            CardinalDirection.UP: [SignD1(), SignT6aRight()],
        }
        super().__init__(control_elements)
