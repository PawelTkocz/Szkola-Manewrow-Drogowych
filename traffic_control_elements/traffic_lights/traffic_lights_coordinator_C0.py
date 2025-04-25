from traffic_control_elements.traffic_lights.traffic_lights_coordinator import (
    TrafficLightsCoordinator,
    TrafficLightsState,
)


class TrafficLightsCoordinatorC0(TrafficLightsCoordinator):
    def get_state(self, tick: int) -> TrafficLightsState:
        if tick // 80 % 2 == 0:
            return TrafficLightsState.GREEN
        return TrafficLightsState.RED
