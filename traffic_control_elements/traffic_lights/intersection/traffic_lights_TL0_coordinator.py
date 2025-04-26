from schemas import CardinalDirection
from traffic_control_elements.traffic_lights.constants import (
    BOTH_RED_LIGHTS_DURATION,
    RED_YELLOW_LIGHT_DURATION,
    YELLOW_LIGHT_DURATION,
)
from traffic_control_elements.traffic_lights.intersection.traffic_lights_coordinator import (
    IntersectionTrafficLightsCoordinator,
    TrafficLightsCyclePhase,
)
from traffic_control_elements.traffic_lights.schemas import TrafficLightsState

GREEN_LIGHT_DURATION = 100
CYCLE: list[TrafficLightsCyclePhase] = [
    {
        "duration": GREEN_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.GREEN,
            CardinalDirection.RIGHT: TrafficLightsState.GREEN,
            CardinalDirection.UP: TrafficLightsState.RED,
            CardinalDirection.DOWN: TrafficLightsState.RED,
        },
    },
    {
        "duration": YELLOW_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.YELLOW,
            CardinalDirection.RIGHT: TrafficLightsState.YELLOW,
            CardinalDirection.UP: TrafficLightsState.RED,
            CardinalDirection.DOWN: TrafficLightsState.RED,
        },
    },
    {
        "duration": BOTH_RED_LIGHTS_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED,
            CardinalDirection.RIGHT: TrafficLightsState.RED,
            CardinalDirection.UP: TrafficLightsState.RED,
            CardinalDirection.DOWN: TrafficLightsState.RED,
        },
    },
    {
        "duration": RED_YELLOW_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED,
            CardinalDirection.RIGHT: TrafficLightsState.RED,
            CardinalDirection.UP: TrafficLightsState.RED_YELLOW,
            CardinalDirection.DOWN: TrafficLightsState.RED_YELLOW,
        },
    },
    {
        "duration": GREEN_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED,
            CardinalDirection.RIGHT: TrafficLightsState.RED,
            CardinalDirection.UP: TrafficLightsState.GREEN,
            CardinalDirection.DOWN: TrafficLightsState.GREEN,
        },
    },
    {
        "duration": YELLOW_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED,
            CardinalDirection.RIGHT: TrafficLightsState.RED,
            CardinalDirection.UP: TrafficLightsState.YELLOW,
            CardinalDirection.DOWN: TrafficLightsState.YELLOW,
        },
    },
    {
        "duration": BOTH_RED_LIGHTS_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED,
            CardinalDirection.RIGHT: TrafficLightsState.RED,
            CardinalDirection.UP: TrafficLightsState.RED,
            CardinalDirection.DOWN: TrafficLightsState.RED,
        },
    },
    {
        "duration": RED_YELLOW_LIGHT_DURATION,
        "lights_states": {
            CardinalDirection.LEFT: TrafficLightsState.RED_YELLOW,
            CardinalDirection.RIGHT: TrafficLightsState.RED_YELLOW,
            CardinalDirection.UP: TrafficLightsState.RED,
            CardinalDirection.DOWN: TrafficLightsState.RED,
        },
    },
]


class TrafficLightsTL0Coordinator(IntersectionTrafficLightsCoordinator):
    def __init__(self) -> None:
        super().__init__(CYCLE)
