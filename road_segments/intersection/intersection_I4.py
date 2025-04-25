from road_segments.intersection.intersection import Intersection
from traffic_control_elements.traffic_lights.intersection_traffic_lights import (
    IntersectionTrafficLights,
)
from traffic_control_elements.traffic_lights.traffic_lights_C0 import TrafficLightsC0


class IntersectionI4(Intersection):
    def __init__(self) -> None:
        super().__init__(
            traffic_lights=IntersectionTrafficLights(
                TrafficLightsC0(0),
                TrafficLightsC0(80),
                TrafficLightsC0(0),
                TrafficLightsC0(80),
            )
        )
