import os
from animations.animation_strategy import AnimationStrategy
from animations.schemas import (
    CarStartingPosition,
    RuntimeAnimationCarInfo,
)
from car.car import Car
from car.toyota_yaris import ToyotaYaris
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
from road_control_center.road_control_center import RoadControlCenter
from traffic_control_center.traffic_control_center import (
    SmartTrafficCar,
    TrafficControlCenter,
)
from constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as general_car_movement_directory,
)
from animations.intersection.constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as intersection_car_movement_directory,
)


class RuntimeAnimation(AnimationStrategy):
    def __init__(
        self,
        manoeuvre_directory_name: str,
        road_control_center: RoadControlCenter,
    ):
        super().__init__(manoeuvre_directory_name)
        self.traffic_control_center = TrafficControlCenter(road_control_center)
        self.cars: list[RuntimeAnimationCarInfo] = []

    def add_car(
        self,
        registry_number: str,
        color: str,
        starting_position: CarStartingPosition,
        manoeuvre_description: IntersectionManoeuvreDescription,
        start_frame_number: int,
    ):
        car = SmartTrafficCar(
            self.traffic_control_center,
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
                "movement_history": [],
                "start_frame_number": start_frame_number,
            }
        )

    def move_cars(self, frame_number: int) -> list[Car]:
        for car in self.cars:
            if frame_number >= car["start_frame_number"]:
                car["movement_history"].append(car["car"].tick())
        return [car["car"] for car in self.cars]

    def _save_cars_movement(self):
        for car_info in self.cars:
            if not os.path.exists(general_car_movement_directory):
                os.makedirs(general_car_movement_directory)
            intersection_directory = os.path.join(
                general_car_movement_directory, intersection_car_movement_directory
            )
            if not os.path.exists(intersection_directory):
                os.makedirs(intersection_directory)
            intersection_manoeuvre_directory = os.path.join(
                intersection_directory, self.manoeuvre_directory_name
            )
            if not os.path.exists(intersection_manoeuvre_directory):
                os.makedirs(intersection_manoeuvre_directory)
            file_path = os.path.join(
                intersection_manoeuvre_directory,
                f"car{car_info['car'].registry_number}.txt",
            )
            with open(file_path, "w") as file:
                for mod in car_info["movement_history"]:
                    file.write(f"{mod[0].name} {mod[1].name}\n")

    def handle_quit(self) -> None:
        self._save_cars_movement()
