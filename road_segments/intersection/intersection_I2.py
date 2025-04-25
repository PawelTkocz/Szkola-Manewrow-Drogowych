from road_segments.intersection.intersection import Intersection
from schemas import CardinalDirection
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_signs.signs import SignB20, SignD1


class IntersectionI2(Intersection):
    def __init__(self) -> None:
        control_elements: dict[CardinalDirection, list[TrafficControlElement]] = {
            CardinalDirection.DOWN: [SignB20()],
            CardinalDirection.LEFT: [SignD1()],
            CardinalDirection.RIGHT: [SignD1()],
            CardinalDirection.UP: [SignB20()],
        }
        super().__init__(control_elements)
