from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModel
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.schemas import LiveCarData


class TrafficControlCenter:
    def __init__(self, road_control_center: RoadControlCenter) -> None:
        self._road_control_center = road_control_center
        self._time = 0
        self.registered_car_models: set[str] = set()

    def send_movement_instruction(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions | None:
        road_control_center = self._get_current_road_control_center(live_car_data)
        return (
            road_control_center.send_movement_instruction(live_car_data)
            if road_control_center
            and self._is_car_model_registered(live_car_data["specification"]["model"])
            else None
        )

    def _is_car_model_registered(self, car_model: CarModel) -> bool:
        return car_model.name in self.registered_car_models

    def _get_current_road_control_center(
        self, live_car_data: LiveCarData
    ) -> RoadControlCenter | None:
        """Based on car position, determine which road control center should give it movement instruction."""
        return (
            self._road_control_center
            if self._road_control_center.is_car_inside_control_area(live_car_data)
            else None
        )

    def register_car_model(self, car_model: CarModel) -> None:
        if self._road_control_center.register_car_model(car_model):
            self.registered_car_models.add(car_model.name)

    def tick(self) -> None:
        self._time += 1
        self._road_control_center.tick(self._time)
