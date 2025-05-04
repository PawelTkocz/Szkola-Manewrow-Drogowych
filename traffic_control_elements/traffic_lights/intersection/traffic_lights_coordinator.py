from typing import TypedDict

from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState


class TrafficLightsCyclePhase(TypedDict):
    lights_states: dict[CardinalDirection, TrafficLightsState]
    duration: int


class IntersectionTrafficLightsCoordinator:
    def __init__(self, cycle: list[TrafficLightsCyclePhase]) -> None:
        if not cycle:
            raise ValueError("Traffic lights cycle must contain at least one phase")
        self.cycle = cycle
        self.cycle_duration = sum(cycle_phase["duration"] for cycle_phase in self.cycle)
        self.phase_end_ticks = self._compute_phase_end_ticks()

    def _compute_phase_end_ticks(self) -> list[int]:
        phase_end_ticks = [self.cycle[0]["duration"]]
        for cycle_phase in self.cycle[1:]:
            phase_end_ticks.append(phase_end_ticks[-1] + cycle_phase["duration"])
        return phase_end_ticks

    def get_states(
        self, tick_number: int
    ) -> dict[CardinalDirection, TrafficLightsState]:
        tick = tick_number % self.cycle_duration
        for i in range(len(self.cycle)):
            if tick < self.phase_end_ticks[i]:
                return self.cycle[i]["lights_states"]
        raise RuntimeError("Tick does not match any phase")
