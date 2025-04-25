from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_signs.signs import SignA5


class IntersectionI0(Intersection):
    def __init__(self) -> None:
        control_elements: dict[CardinalDirection, list[TrafficControlElement]] = {
            CardinalDirection.DOWN: [SignA5()],
            CardinalDirection.LEFT: [SignA5()],
            CardinalDirection.RIGHT: [SignA5()],
            CardinalDirection.UP: [SignA5()],
        }
        super().__init__(control_elements)
