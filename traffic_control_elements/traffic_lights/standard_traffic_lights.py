from traffic_control_elements.traffic_lights.schemas import TrafficLightsState
from traffic_control_elements.traffic_lights.traffic_lights import TrafficLights

WIDTH = 25
HEIGHT = 68


class StandardTrafficLights(TrafficLights):
    def __init__(self, start_state: TrafficLightsState) -> None:
        states_images_file_names: dict[TrafficLightsState, str] = {
            TrafficLightsState.GREEN: "traffic_lights_green.png",
            TrafficLightsState.YELLOW: "traffic_lights_yellow.png",
            TrafficLightsState.RED: "traffic_lights_red.png",
            TrafficLightsState.RED_YELLOW: "traffic_lights_red_yellow.png",
        }
        super().__init__(states_images_file_names, WIDTH, HEIGHT, start_state)
