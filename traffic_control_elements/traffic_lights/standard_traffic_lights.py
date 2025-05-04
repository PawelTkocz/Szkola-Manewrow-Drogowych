from traffic_control_elements.traffic_lights.schemas import TrafficLightsState
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights

WIDTH = 25
HEIGHT = 68


class StandardTrafficLights(TrafficLights):
    def __init__(self, start_state: TrafficLightsState) -> None:
        state_image_filenames: dict[TrafficLightsState, str] = {
            TrafficLightsState.GREEN: "standard_lights_green.png",
            TrafficLightsState.YELLOW: "standard_lights_yellow.png",
            TrafficLightsState.RED: "standard_lights_red.png",
            TrafficLightsState.RED_YELLOW: "standard_lights_red_yellow.png",
        }
        super().__init__(state_image_filenames, WIDTH, HEIGHT, start_state)
