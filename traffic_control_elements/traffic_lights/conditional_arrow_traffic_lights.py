from traffic_control_elements.traffic_lights.schemas import (
    TrafficLightsState,
)
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights

WIDTH = 50
HEIGHT = 68


class ConditionalArrowTrafficLights(TrafficLights):
    def __init__(self, start_state: TrafficLightsState) -> None:
        state_image_filenames: dict[TrafficLightsState, str] = {
            TrafficLightsState.GREEN: "arrow_lights_green.png",
            TrafficLightsState.YELLOW: "arrow_lights_yellow.png",
            TrafficLightsState.RED: "arrow_lights_red.png",
            TrafficLightsState.RED_WITH_ARROW: "arrow_lights_arrow_on.png",
            TrafficLightsState.RED_YELLOW: "arrow_lights_red_yellow.png",
        }
        super().__init__(state_image_filenames, WIDTH, HEIGHT, start_state)
