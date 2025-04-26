from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.conditional_arrow_traffic_lights import (
    ConditionalArrowTrafficLights,
)
from traffic_control_elements.traffic_lights.intersection.intersection_traffic_lights import (
    IntersectionTrafficLights,
)
from traffic_control_elements.traffic_lights.intersection.traffic_lights_TL1_coordinator import (
    TrafficLightsTL1Coordinator,
)
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights


class TrafficLightsTL1(IntersectionTrafficLights):
    def __init__(self) -> None:
        lights_coordinator = TrafficLightsTL1Coordinator()
        start_lights_state = lights_coordinator.get_states(0)
        traffic_lights: dict[CardinalDirection, TrafficLights] = {
            side: ConditionalArrowTrafficLights(start_lights_state[side])
            for side in CardinalDirection
        }
        super().__init__(traffic_lights, lights_coordinator)
