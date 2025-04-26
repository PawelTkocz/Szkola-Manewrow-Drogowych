from traffic_control_elements.traffic_lights.schemas import (
    TrafficLightsState,
)
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights

WIDTH = 50
HEIGHT = 68


class ConditionalArrowTrafficLights(TrafficLights):
    def __init__(self, start_state: TrafficLightsState) -> None:
        states_images_file_names: dict[TrafficLightsState, str] = {
            TrafficLightsState.GREEN: "traffic_lights_with_arrow_green.png",
            TrafficLightsState.YELLOW: "traffic_lights_with_arrow_yellow.png",
            TrafficLightsState.RED: "traffic_lights_with_arrow_red0.png",
            TrafficLightsState.RED_WITH_ARROW: "traffic_lights_with_arrow_red.png",
            TrafficLightsState.RED_YELLOW: "traffic_lights_with_arrow_red_yellow.png",
        }
        super().__init__(states_images_file_names, WIDTH, HEIGHT, start_state)
