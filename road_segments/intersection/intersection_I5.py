from road_segments.intersection.intersection import Intersection
from traffic_control_elements.traffic_lights.intersection.traffic_lights_TL1 import (
    TrafficLightsTL1,
)


class IntersectionI5(Intersection):
    def __init__(self) -> None:
        super().__init__(traffic_lights=TrafficLightsTL1())
