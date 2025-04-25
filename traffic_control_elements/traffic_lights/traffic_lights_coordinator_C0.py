from traffic_control_elements.traffic_lights.constants import (
    BOTH_RED_LIGHTS_LENGTH,
    RED_YELLOW_LIGHT_LENGTH,
    YELLOW_LIGHT_LENGTH,
)
from traffic_control_elements.traffic_lights.traffic_lights_coordinator import (
    TrafficLightsCoordinator,
    TrafficLightsState,
)

CYCLE_LENGTH = 200


class TrafficLightsCoordinatorC0(TrafficLightsCoordinator):
    def __init__(self) -> None:
        green_light_length = (
            CYCLE_LENGTH / 2
            - RED_YELLOW_LIGHT_LENGTH
            - BOTH_RED_LIGHTS_LENGTH
            - YELLOW_LIGHT_LENGTH
        )
        if CYCLE_LENGTH % 2 != 0:
            raise ValueError("Cycle must be even number.")
        if green_light_length <= 0:
            raise ValueError("Cycle is to short.")

        self.cycle: list[tuple[TrafficLightsState, int]] = [
            (TrafficLightsState.GREEN, green_light_length),
            (TrafficLightsState.YELLOW, YELLOW_LIGHT_LENGTH),
            (
                TrafficLightsState.RED,
                2 * BOTH_RED_LIGHTS_LENGTH
                + green_light_length
                + RED_YELLOW_LIGHT_LENGTH
                + YELLOW_LIGHT_LENGTH,
            ),
            (TrafficLightsState.RED_YELLOW, RED_YELLOW_LIGHT_LENGTH),
        ]

    def get_state(self, tick: int) -> TrafficLightsState:
        x = tick % CYCLE_LENGTH
        sum = 0
        for state, state_length in self.cycle:
            if state_length + sum > x:
                return state
            sum += state_length
        raise ValueError("sth went wrong")
