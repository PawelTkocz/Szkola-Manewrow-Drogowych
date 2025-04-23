from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_signs.signs import SignA5
from traffic_control_elements.traffic_signs.traffic_sign import TrafficSign


class IntersectionI0(Intersection):
    def __init__(self) -> None:
        control_elements: dict[CardinalDirection, list[TrafficSign]] = {
            CardinalDirection.DOWN: [SignA5()],
            CardinalDirection.LEFT: [SignA5()],
            CardinalDirection.RIGHT: [SignA5()],
            CardinalDirection.UP: [SignA5()],
        }
        super().__init__(control_elements)
