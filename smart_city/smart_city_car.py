from car.car import DEFAULT_CAR_COLORISTICS
from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
)
from car.model import CarModel
from car.schemas import CarColoristics
from geometry.direction import Direction
from geometry.vector import Point
from schemas import HorizontalDirection
from smart_city.schemas import IntersectionManoeuvreDescription, LiveCarData
from smart_city.traffic_control_center import TrafficControlCenter


class SmartCityCar(InstructionControlledCar):
    def __init__(
        self,
        registry_number: str,
        model: CarModel,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_direction: Direction = Direction(Point(1, 0)),
        turn_signal: HorizontalDirection | None = None,
        coloristics: CarColoristics = DEFAULT_CAR_COLORISTICS,
        *,
        color: str | None = None,
        high_priority: bool = False,
    ):
        super().__init__(
            registry_number,
            model,
            front_middle_position,
            direction,
            velocity,
            wheels_direction,
            turn_signal,
            coloristics,
            color=color,
        )
        self.high_priority = high_priority
        self.manoeuvre_description: IntersectionManoeuvreDescription | None = None
        self.traffic_control_center: TrafficControlCenter | None = None
        self.control_instructions_history: list[CarControlInstructions] = []

    def set_manoeuvre(
        self, manoeuvre_description: IntersectionManoeuvreDescription
    ) -> None:
        self.manoeuvre_description = manoeuvre_description

    def apply_control_instructions(
        self, control_instructions: CarControlInstructions
    ) -> None:
        self.control_instructions_history.append(control_instructions)
        return super().apply_control_instructions(control_instructions)

    def tick(self) -> None:
        if self.traffic_control_center:
            control_instructions = (
                self.traffic_control_center.send_control_instructions(
                    self.get_live_data()
                )
            )
            if control_instructions:
                self.apply_control_instructions(control_instructions)
        super().tick()

    def connect_to_traffic_control_center(
        self, traffic_control_center: TrafficControlCenter
    ) -> None:
        self.traffic_control_center = traffic_control_center

    def get_live_data(self) -> LiveCarData:
        return {
            "specification": {
                "registry_number": self.registry_number,
                "model": self.model,
            },
            "live_state": {
                "direction": self.direction,
                "front_middle": self.front_middle,
                "velocity": self.velocity,
                "wheels_direction": self.wheels_direction,
                "high_priority": self.high_priority,
            },
            "manoeuvre_description": self.manoeuvre_description,
        }
