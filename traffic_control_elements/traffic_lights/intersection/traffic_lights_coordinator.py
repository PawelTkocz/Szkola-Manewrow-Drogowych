from typing import TypedDict

from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class TrafficLightsCyclePhase(TypedDict):
    lights_states: dict[CardinalDirection, TrafficLightsState]
    duration: int


class IntersectionTrafficLightsCoordinator:
    def __init__(self, cycle: list[TrafficLightsCyclePhase]) -> None:
        if not cycle:
            raise ValueError("Traffic list cycle must contain at least one phase")
        self.cycle = cycle
        self.cycle_duration = sum(cycle_phase["duration"] for cycle_phase in self.cycle)
        cumulative_durations = [self.cycle[0]["duration"]]
        for cycle_phase in self.cycle[1:]:
            cumulative_durations.append(
                cumulative_durations[-1] + cycle_phase["duration"]
            )
        self.cumulative_durations = cumulative_durations

    def get_states(
        self, tick_number: int
    ) -> dict[CardinalDirection, TrafficLightsState]:
        tick = tick_number % self.cycle_duration
        for i in range(len(self.cycle)):
            if tick < self.cumulative_durations[i]:
                return self.cycle[i]["lights_states"]
        raise ValueError("Failed to get current lights cycle phase")
