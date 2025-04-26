from typing import TypedDict
from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.constants import (
    BOTH_RED_LIGHTS_DURATION,
    RED_YELLOW_LIGHT_DURATION,
    YELLOW_LIGHT_DURATION,
)
from traffic_control_elements.traffic_lights.intersection.traffic_lights_coordinator import (
    IntersectionTrafficLightsCoordinator,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class TrafficLightsCyclePhase(TypedDict):
    horizontal: TrafficLightsState
    vertical: TrafficLightsState
    duration: int


GREEN_LIGHT_DURATION = 100


class TrafficLightsTL0Coordinator(IntersectionTrafficLightsCoordinator):
    def __init__(self) -> None:
        self.cycle: list[TrafficLightsCyclePhase] = [
            {
                "horizontal": TrafficLightsState.GREEN,
                "vertical": TrafficLightsState.RED,
                "duration": GREEN_LIGHT_DURATION,
            },
            {
                "horizontal": TrafficLightsState.YELLOW,
                "vertical": TrafficLightsState.RED,
                "duration": YELLOW_LIGHT_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED,
                "vertical": TrafficLightsState.RED,
                "duration": BOTH_RED_LIGHTS_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED,
                "vertical": TrafficLightsState.RED_YELLOW,
                "duration": RED_YELLOW_LIGHT_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED,
                "vertical": TrafficLightsState.GREEN,
                "duration": GREEN_LIGHT_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED,
                "vertical": TrafficLightsState.YELLOW,
                "duration": YELLOW_LIGHT_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED,
                "vertical": TrafficLightsState.RED,
                "duration": BOTH_RED_LIGHTS_DURATION,
            },
            {
                "horizontal": TrafficLightsState.RED_YELLOW,
                "vertical": TrafficLightsState.RED,
                "duration": RED_YELLOW_LIGHT_DURATION,
            },
        ]
        self.cycle_duration = sum(cycle_phase["duration"] for cycle_phase in self.cycle)
        cumulative_ticks = [self.cycle[0]["duration"]]
        for cycle_phase in self.cycle[1:]:
            cumulative_ticks.append(cumulative_ticks[-1] + cycle_phase["duration"])
        self.cumulative_phase_ticks = cumulative_ticks

    def get_states(
        self, tick_number: int
    ) -> dict[CardinalDirection, TrafficLightsState]:
        current_cycle_phase = self.get_current_cycle_phase(tick_number)
        return {
            CardinalDirection.DOWN: current_cycle_phase["vertical"],
            CardinalDirection.UP: current_cycle_phase["vertical"],
            CardinalDirection.LEFT: current_cycle_phase["horizontal"],
            CardinalDirection.RIGHT: current_cycle_phase["horizontal"],
        }

    def get_current_cycle_phase(self, tick_number: int) -> TrafficLightsCyclePhase:
        tick = tick_number % self.cycle_duration
        for i in range(len(self.cycle)):
            if tick < self.cumulative_phase_ticks[i]:
                return self.cycle[i]
        raise ValueError("Failed to get current lights cycle phase")
