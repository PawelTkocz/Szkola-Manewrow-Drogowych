from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.constants import (
    ALL_LIGHTS_RED_DURATION,
    RED_YELLOW_LIGHT_DURATION,
    YELLOW_LIGHT_DURATION,
)
from traffic_control_elements.traffic_lights.intersection.traffic_lights_coordinator import (
    IntersectionTrafficLightsCoordinator,
    TrafficLightsCyclePhase,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState
from utils import clockwise_direction_shift

GREEN_LIGHT_DURATION = 100


class TrafficLightsTL1Coordinator(IntersectionTrafficLightsCoordinator):
    def __init__(self) -> None:
        cycle = []
        for side in CardinalDirection:
            cycle.extend(self._get_cycle_quarter(side))
        super().__init__(cycle)

    def _get_cycle_quarter(
        self, side: CardinalDirection
    ) -> list[TrafficLightsCyclePhase]:
        return [
            {
                "duration": RED_YELLOW_LIGHT_DURATION,
                "lights_states": {
                    side: TrafficLightsState.RED_YELLOW,
                    clockwise_direction_shift(side, 2): TrafficLightsState.RED,
                    clockwise_direction_shift(side, 1): TrafficLightsState.RED,
                    clockwise_direction_shift(side, 3): TrafficLightsState.RED,
                },
            },
            {
                "duration": GREEN_LIGHT_DURATION,
                "lights_states": {
                    side: TrafficLightsState.GREEN,
                    clockwise_direction_shift(
                        side, 2
                    ): TrafficLightsState.RED_WITH_ARROW,
                    clockwise_direction_shift(side, 1): TrafficLightsState.RED,
                    clockwise_direction_shift(side, 3): TrafficLightsState.RED,
                },
            },
            {
                "duration": YELLOW_LIGHT_DURATION,
                "lights_states": {
                    side: TrafficLightsState.YELLOW,
                    clockwise_direction_shift(
                        side, 2
                    ): TrafficLightsState.RED_WITH_ARROW,
                    clockwise_direction_shift(side, 1): TrafficLightsState.RED,
                    clockwise_direction_shift(side, 3): TrafficLightsState.RED,
                },
            },
            {
                "duration": ALL_LIGHTS_RED_DURATION,
                "lights_states": {
                    side: TrafficLightsState.RED for side in CardinalDirection
                },
            },
        ]
