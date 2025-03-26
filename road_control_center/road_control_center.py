from car.instruction_controlled_car import MovementInstruction
from road_control_center.road_car_controller import RoadCarController
from smart_city.schemas import LiveCarData
from traffic_control_center_software.car_movement_simulator import (
    get_predicted_live_car_data,
)


class RoadControlCenter(RoadCarController):
    def __init__(self):
        self.time = 0
        self.live_cars_data: dict[str, LiveCarData] = {}
        self._predicted_live_cars_data: dict[str, LiveCarData] = {}

    def tick(self, current_time: int) -> None:
        self._time = current_time
        self.live_cars_data = self._predicted_live_cars_data
        self._predicted_live_cars_data = {}
        self.update_active_cars_on_road(self.live_cars_data)

    def send_movement_instruction(
        self, live_car_data: LiveCarData
    ) -> MovementInstruction:
        registry_number = live_car_data["registry_number"]
        if registry_number not in self.live_cars_data:
            self.register_new_active_car(live_car_data)
        self.live_cars_data[registry_number] = live_car_data
        movement_instruction = self.calculate_movement_instruction(registry_number)
        self._predicted_live_cars_data[registry_number] = get_predicted_live_car_data(
            live_car_data, movement_instruction
        )
        return movement_instruction
