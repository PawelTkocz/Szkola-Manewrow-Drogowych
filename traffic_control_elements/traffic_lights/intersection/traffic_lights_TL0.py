from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.intersection.intersection_traffic_lights import (
    IntersectionTrafficLights,
)
from traffic_control_elements.traffic_lights.intersection.traffic_lights_TL0_coordinator import (
    TrafficLightsTL0Coordinator,
)
from traffic_control_elements.traffic_lights.standard_traffic_lights import (
    StandardTrafficLights,
)
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights


class TrafficLightsTL0(IntersectionTrafficLights):
    def __init__(self) -> None:
        lights_coordinator = TrafficLightsTL0Coordinator()
        start_lights_state = lights_coordinator.get_states(0)
        traffic_lights: dict[CardinalDirection, TrafficLights] = {
            side: StandardTrafficLights(start_lights_state[side])
            for side in CardinalDirection
        }
        super().__init__(traffic_lights, lights_coordinator)
