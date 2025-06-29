from car.instruction_controlled_car import CarControlInstructions
from car.model import CarModelSpecification
from traffic_control_system.road_control_center.road_control_center import (
    RoadControlCenter,
)
from traffic_control_system.schemas import LiveCarData


class TrafficControlCenter:
    def __init__(self, road_control_center: RoadControlCenter) -> None:
        self._road_control_center = road_control_center
        road_control_center.register_tracks()
        self._time = 0
        self.registered_car_models: set[str] = set()

    def send_control_instructions(
        self, live_car_data: LiveCarData
    ) -> CarControlInstructions | None:
        road_control_center = self._get_current_road_control_center(live_car_data)
        return (
            road_control_center.send_control_instructions(live_car_data)
            if road_control_center
            and self._is_car_model_registered(live_car_data["specification"]["model"])
            else None
        )

    def _is_car_model_registered(
        self, car_model_specification: CarModelSpecification
    ) -> bool:
        return car_model_specification["name"] in self.registered_car_models

    def _get_current_road_control_center(
        self, live_car_data: LiveCarData
    ) -> RoadControlCenter | None:
        return (
            self._road_control_center
            if self._road_control_center.is_car_inside_control_area(live_car_data)
            else None
        )

    def register_car_model(
        self, car_model_specification: CarModelSpecification
    ) -> None:
        if self._road_control_center.register_car_model(car_model_specification):
            self.registered_car_models.add(car_model_specification["name"])

    def tick(self) -> None:
        self._time += 1
        self._road_control_center.tick(self._time)
