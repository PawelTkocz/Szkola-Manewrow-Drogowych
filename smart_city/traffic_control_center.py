from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModel
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.schemas import LiveCarData


class TrafficControlCenter:
    def __init__(self, road_control_center: RoadControlCenter):
        self._road_control_center = road_control_center
        self._time = 0

    def send_movement_instruction(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions:
        road_control_center = self._get_current_road_control_center(live_car_data)
        return road_control_center.send_movement_instruction(live_car_data)

    def _get_current_road_control_center(
        self, live_car_data: LiveCarData
    ) -> RoadControlCenter:
        """Based on car position, determine which road control center should give it movement instruction."""
        return self._road_control_center

    # def register_car_model(self, car_model: CarModel) -> None:
    #     self._road_control_center.register_car_model(car_model)

    def tick(self) -> None:
        self._time += 1
        self._road_control_center.tick(self._time)
