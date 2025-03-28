import os

from animations.animations_generators.animation_strategy import AnimationStrategy
from animations.animations_generators.schemas import (
    CarStartingPosition,
    RuntimeAnimationCarInfo,
)
from car.car import Car
from car.toyota_yaris import ToyotaYaris
from smart_city.road_control_center.manoeuvres.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.road_control_center.road_control_center import RoadControlCenter
from smart_city.smart_city_car import SmartCityCar
from smart_city.traffic_control_center import (
    TrafficControlCenter,
)


class RuntimeAnimation(AnimationStrategy):
    def __init__(
        self,
        movement_instructions_dir_path: str,
        road_control_center: RoadControlCenter,
    ) -> None:
        super().__init__(movement_instructions_dir_path)
        self.traffic_control_center = TrafficControlCenter(road_control_center)
        self.cars: list[RuntimeAnimationCarInfo] = []

    def add_car(
        self,
        registry_number: str,
        color: str,
        starting_position: CarStartingPosition,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ) -> None:
        car = SmartCityCar(
            manoeuvre_description,
            registry_number,
            ToyotaYaris(),
            color,
            starting_position["front_middle"],
            starting_position["direction"],
        )
        self.cars.append(
            {
                "car": car,
                "movement_instructions": [],
                "start_frame_number": start_frame_number,
            }
        )

    def move_cars(self, frame_number: int) -> list[Car]:
        for car in self._get_cars_that_start_movement(frame_number):
            car["car"].connect_to_traffic_control_center(self.traffic_control_center)
        self.traffic_control_center.tick()
        for car in self.cars:
            if frame_number < car["start_frame_number"]:
                continue
            movement_instruction = car["car"].tick()
            if movement_instruction:
                car["movement_instructions"].append(movement_instruction)
        return [car["car"] for car in self.cars]

    def _get_cars_that_start_movement(
        self, frame_number: int
    ) -> list[RuntimeAnimationCarInfo]:
        return [car for car in self.cars if car["start_frame_number"] == frame_number]

    def _save_movement_instructions(self) -> None:
        os.makedirs(self.movement_instructions_dir_path, exist_ok=True)
        for car in self.cars:
            file_path = os.path.join(
                self.movement_instructions_dir_path,
                f"car_{car['car'].registry_number}.txt",
            )
            with open(file_path, "w") as file:
                for movement_instruction in car["movement_instructions"]:
                    file.write(
                        f"{movement_instruction['speed_instruction'].name} {movement_instruction['turn_instruction'].name}\n"
                    )

    def handle_quit(self) -> None:
        self._save_movement_instructions()
