from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
)
from car.model import CarModel
from geometry import Direction, Point
from smart_city.road_control_center.intersection.intersection_manoeuvre.schemas import (
    IntersectionManoeuvreDescription,
)
from smart_city.schemas import LiveCarData
from smart_city.traffic_control_center import TrafficControlCenter


class SmartCityCar(InstructionControlledCar):
    def __init__(
        self,
        manoeuvre_description: IntersectionManoeuvreDescription,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
        wheels_direction: Direction = Direction(Point(1, 0)),
        high_priority: bool = False,
    ):
        super().__init__(
            registry_number,
            model,
            color,
            front_middle_position,
            direction,
            velocity,
            wheels_direction,
        )
        self.high_priority = high_priority
        self.manoeuvre_description = manoeuvre_description
        self.traffic_control_center: TrafficControlCenter | None = None

    def tick(self) -> CarControlInstructions | None:
        movement_instruction = self.fetch_movement_instruction()
        super().tick(movement_instruction)
        return movement_instruction

    def connect_to_traffic_control_center(
        self, traffic_control_center: TrafficControlCenter
    ) -> None:
        self.traffic_control_center = traffic_control_center

    def fetch_movement_instruction(self) -> CarControlInstructions | None:
        return (
            self.traffic_control_center.send_movement_instruction(self.get_live_data())
            if self.traffic_control_center
            else None
        )

    def get_live_data(self) -> LiveCarData:
        return {
            "specification": {
                "registry_number": self.registry_number,
                "color": self.color,
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
