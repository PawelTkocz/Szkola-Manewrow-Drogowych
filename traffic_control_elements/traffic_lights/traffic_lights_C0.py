from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights
from traffic_control_elements.traffic_lights.traffic_lights_coordinator import (
    TrafficLightsState,
)
from traffic_control_elements.traffic_lights.traffic_lights_coordinator_C0 import (
    TrafficLightsCoordinatorC0,
)


class TrafficLightsC0(TrafficLights):
    def __init__(self, start_tick: int) -> None:
        states_images_file_names: dict[TrafficLightsState, str] = {
            TrafficLightsState.GREEN: "traffic_lights_green.png",
            TrafficLightsState.YELLOW: "traffic_lights_yellow.png",
            TrafficLightsState.RED: "traffic_lights_red.png",
            TrafficLightsState.RED_YELLOW: "traffic_lights_red_yellow.png",
        }
        super().__init__(
            states_images_file_names, start_tick, TrafficLightsCoordinatorC0()
        )
