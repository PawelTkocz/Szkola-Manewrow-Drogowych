from car.car import DEFAULT_CAR_COLORS
from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
)
from car.model import CarModelSpecification
from car.schemas import CarColors
from geometry.direction import Direction
from geometry.vector import Point
from smart_city.schemas import IntersectionManoeuvreDescription, LiveCarData
from smart_city.traffic_control_center import TrafficControlCenter


class SmartCityCar(InstructionControlledCar):
    def __init__(
        self,
        registry_number: str,
        model_specification: CarModelSpecification,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_angle: float = 0,
        coloristics: CarColors = DEFAULT_CAR_COLORS,
        *,
        color: str | None = None,
        high_priority: bool = False,
    ):
        super().__init__(
            registry_number,
            model_specification,
            front_middle_position,
            direction,
            velocity,
            wheels_angle,
            coloristics,
            shell_color=color,
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
                "model": self.specification,
            },
            "live_state": {
                "direction": self.direction,
                "front_middle": self.front_middle,
                "velocity": self.velocity,
                "high_priority": self.high_priority,
                "wheels_angle": self.wheels_angle,
                "turn_signal": self.turn_signal,
            },
            "manoeuvre_description": self.manoeuvre_description,
        }
