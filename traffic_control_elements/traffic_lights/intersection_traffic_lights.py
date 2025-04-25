from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights
from traffic_control_elements.traffic_lights.traffic_lights_coordinator import (
    TrafficLightsState,
)


class IntersectionTrafficLights:
    def __init__(
        self,
        left_lights: TrafficLights,
        up_lights: TrafficLights,
        right_lights: TrafficLights,
        down_lights: TrafficLights,
    ) -> None:
        self._traffic_lights: dict[CardinalDirection, TrafficLights] = {
            CardinalDirection.LEFT: left_lights,
            CardinalDirection.UP: up_lights,
            CardinalDirection.RIGHT: right_lights,
            CardinalDirection.DOWN: down_lights,
        }

    def get_ligths(self) -> dict[CardinalDirection, TrafficLights]:
        return self._traffic_lights

    def get_lights_states(self) -> dict[CardinalDirection, TrafficLightsState]:
        return {
            side: self._traffic_lights[side].get_state() for side in CardinalDirection
        }
