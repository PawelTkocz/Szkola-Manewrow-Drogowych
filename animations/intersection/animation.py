import os
from typing import TypedDict
from car.autonomous_car import AutonomousCar
from car.autonomous.intersection_program_alpha import IntersectionProgram
from car.autonomous.program import AutonomousDrivingProgram
from car.car import LiveCarData, SpeedModifications
from car.toyota_yaris import ToyotaYaris
from geometry import Directions, Point
from intersection.intersection import Intersection
from state import State
from constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as general_car_movement_directory,
)
from animations.intersection.constants import (
    SAVED_CAR_MOVEMENT_DIRECTORY as intersection_car_movement_directory,
)


class AnimationCarInfo(TypedDict):
    car_id: int
    car: AutonomousCar
    movement_history: list[tuple[Directions, SpeedModifications]]
    start_frame_number: int


class IntersectionAnimation(State):
    def __init__(
        self,
        previous_state: State,
        intersection: Intersection,
        manoeuvre_directory_name: str,
        read_saved_cars_movement: bool,
    ):
        super().__init__(previous_state=previous_state)
        self.intersection = intersection
        self.manoeuvre_directory_name = manoeuvre_directory_name
        self.read_saved_cars_movement = read_saved_cars_movement
        self.cars: list[AnimationCarInfo] = []
        self.frames_counter = 0

    def add_car(
        self,
        color: str,
        starting_side: Directions,
        ending_side: Directions,
        start_frame_number: int,
    ):
        front_middle_position = self.intersection.intersection_parts["incoming_lines"][starting_side].rear_middle
        direction = self.intersection.intersection_parts["incoming_lines"][starting_side].direction
        model = ToyotaYaris()
        autonomous_driving_program = AutonomousDrivingProgram(model, IntersectionProgram(), None)
        car = AutonomousCar(
            ToyotaYaris(),
            color,
            front_middle_position,
            autonomous_driving_program,
            direction,
        )
        car_id = len(self.cars) + 1
        movement_history = (
            self.load_saved_car_movement(car_id)
            if self.read_saved_cars_movement
            else []
        )
        self.cars.append(
            {"car_id": car_id, "car": car, "movement_history": movement_history, "start_frame_number": start_frame_number}
        )
        self.intersection.add_car(car.get_live_data(), starting_side, ending_side)

    def save_cars_movement(self):
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
            car_id = car_info["car_id"]
            file_path = os.path.join(
                intersection_manoeuvre_directory, f"car{car_id}.txt"
            )
            with open(file_path, "w") as file:
                for mod in car_info["movement_history"]:
                    file.write(f"{mod[0].name} {mod[1].name}\n")

    def load_saved_car_movement(self, car_id: int):
        file_path = os.path.join(
            general_car_movement_directory,
            intersection_car_movement_directory,
            self.manoeuvre_directory_name,
            f"car{car_id}.txt",
        )
        with open(file_path, "r") as file:
            return [tuple(line.split()) for line in file]

    def move_cars(self):
        if not self.read_saved_cars_movement:
            for car_info in self.cars:
                if self.frames_counter >= car_info["start_frame_number"]:
                    car_info["movement_history"].append(car_info["car"].move())
            return
        for car_info in self.cars:
            if self.frames_counter < car_info["start_frame_number"]:
                continue
            saved_movement_decision_index = self.frames_counter - car_info["start_frame_number"]
            if saved_movement_decision_index >= len(car_info["movement_history"]):
                continue
            turn_direction, speed_modification = car_info["movement_history"][
                saved_movement_decision_index
            ]
            car_info["car"].move(movement_decision={
                "speed_modification": SpeedModifications[speed_modification],
                "turn_direction": Directions[turn_direction]
            })

    def draw(self, screen):
        self.intersection.draw(screen)
        for car_info in self.cars:
            car_info["car"].draw(screen)

    def render_frame(self, screen):
        self.draw(screen)
        self.move_cars()
        self.frames_counter += 1

    def handle_click(self, mouse_click_position) -> State:
        return self.previous_state

    def handle_quit(self):
        if not self.read_saved_cars_movement:
            self.save_cars_movement()
