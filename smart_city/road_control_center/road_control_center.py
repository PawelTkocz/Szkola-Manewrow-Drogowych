from car.instruction_controlled_car import CarControlInstructions
from road_segments.road_segment import RoadSegment
from smart_city.road_control_center.road_car_controller import RoadCarController
from smart_city.road_control_center.utils import (
    get_predicted_live_car_data,
)
from smart_city.schemas import LiveCarData


class RoadControlCenter(RoadCarController):
    def __init__(self, road_segment: RoadSegment, id: str) -> None:
        self.id = id
        self.time = 0
        self.live_cars_data: dict[str, LiveCarData] = {}
        self._predicted_live_cars_data: dict[str, LiveCarData] = {}
        self.road_segment = road_segment

    def is_car_inside_control_area(self, live_car_data: LiveCarData) -> bool:
        return self.road_segment.area.is_point_inside(
            live_car_data["live_state"]["front_middle"]
        )

    def tick(self, current_time: int) -> None:
        self._time = current_time
        self.live_cars_data = self._predicted_live_cars_data
        self._predicted_live_cars_data = {}
        self.update_active_cars_on_road(list(self.live_cars_data))
        self.road_segment.tick()

    def send_control_instructions(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions:
        registry_number = live_car_data["specification"]["registry_number"]
        if registry_number not in self.live_cars_data:
            self.register_new_active_car(live_car_data)
        self.live_cars_data[registry_number] = live_car_data
        control_instructions = self.calculate_control_instructions(registry_number)
        self._predicted_live_cars_data[registry_number] = get_predicted_live_car_data(
            live_car_data, control_instructions["movement_instructions"]
        )
        return control_instructions
