from car.instruction_controlled_car import InstructionControlledCar, MovementInstruction
from car.model import CarModel
from geometry import Direction, Point
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription
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
    ):
        super().__init__(
            registry_number, model, color, front_middle_position, direction, velocity
        )
        self.manoeuvre_description = manoeuvre_description
        self.traffic_control_center: TrafficControlCenter | None = None

    def tick(self) -> MovementInstruction | None:
        movement_instruction = self.fetch_movement_instruction()
        if movement_instruction:
            self.apply_movement_instruction(movement_instruction)
        self.move()
        return movement_instruction

    def connect_to_traffic_control_center(
        self, traffic_control_center: TrafficControlCenter
    ) -> None:
        self.traffic_control_center = traffic_control_center

    def fetch_movement_instruction(self) -> MovementInstruction | None:
        return (
            self.traffic_control_center.send_movement_instruction(self.get_live_data())
            if self.traffic_control_center
            else None
        )

    def get_live_data(self) -> LiveCarData:
        return {
            "length": self.length,
            "width": self.width,
            "direction": self.direction,
            "front_middle": self.front_middle,
            "front_right": self.front_right,
            "front_left": self.front_left,
            "rear_middle": self.rear_middle,
            "rear_left": self.rear_left,
            "rear_right": self.rear_right,
            "color": self.color,
            "model": self.model,
            "wheels_angle": self.wheels_angle,
            "max_acceleration": self.max_acceleration,
            "velocity": self.velocity,
            "max_velocity": self.max_velocity,
            "max_brake": self.max_brake,
            "registry_number": self.registry_number,
            "manoeuvre_description": self.manoeuvre_description,
        }
