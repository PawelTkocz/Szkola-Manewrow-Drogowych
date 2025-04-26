from typing import Mapping
from schemas import CardinalDirection
from traffic_control_elements.traffic_control_element import TrafficControlElement
from traffic_control_elements.traffic_lights.intersection.traffic_lights_coordinator import (
    IntersectionTrafficLightsCoordinator,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights


class IntersectionTrafficLights:
    def __init__(
        self,
        traffic_lights: dict[CardinalDirection, TrafficLights],
        traffic_lights_coordinator: IntersectionTrafficLightsCoordinator,
    ) -> None:
        self._current_tick = 0
        self._traffic_lights = traffic_lights
        self._traffic_lights_coordinator = traffic_lights_coordinator

    def get_ligths(self) -> dict[CardinalDirection, TrafficLights]:
        return self._traffic_lights

    def get_lights_states(self) -> dict[CardinalDirection, TrafficLightsState]:
        return {
            side: self._traffic_lights[side].get_state()
            for side in self._traffic_lights
        }

    def tick(self) -> None:
        self._current_tick += 1
        lights_states = self._traffic_lights_coordinator.get_states(self._current_tick)
        for side in self._traffic_lights:
            self._traffic_lights[side].set_state(lights_states[side])
