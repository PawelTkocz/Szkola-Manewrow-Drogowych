from typing import TypedDict
from car.car import Car, SpeedModifications
from car.model import CarModel
from geometry import Direction, Directions, Point
from road_control_center.intersection.schemas import IntersectionManoeuvreDescription, MovementInstruction
from traffic_control_center.traffic_control_center import TrafficControlCenter

class LiveCarData(TypedDict):
    registry_number: int
    velocity: float
    front_middle: Point
    direction: Point
    front_left: Point
    front_right: Point
    rear_left: Point
    rear_middle: Point
    rear_right: Point
    wheels_angle: Point
    length: float
    width: float
    max_acceleration: float
    max_velocity: float
    max_brake: float
    model: CarModel
    color: str
    manoeuvres: dict[str, IntersectionManoeuvreDescription] # manoeuvre per road segment id

class CarDataTransmitter:
    def __init__(self, autonomous_car: "AutonomousCar"):
        self._autonomous_car = autonomous_car
        self.traffic_control_center = None

    def set_traffic_control_center(self, traffic_control_center: TrafficControlCenter):
        self.traffic_control_center = traffic_control_center

    def get_movement_instruction(self) -> MovementInstruction:
        return self.traffic_control_center.send_movement_instruction(self._autonomous_car.registry_number)

    def get_live_car_data(self) -> LiveCarData:
        return self._autonomous_car.get_live_data()

class AutonomousCar(Car):
    def __init__(
        self,
        registry_number: str,
        model: CarModel,
        color: str,
        front_middle_position: Point,
        direction: Direction = Direction(Point(1, 0)),
        velocity: float = 0,
    ):
        super().__init__(registry_number, model, color, front_middle_position, direction, velocity)
        self.car_data_transmitter = CarDataTransmitter(self)
        self.manoeuvres_description = {
            "Intersection_A0": {
                "starting_side": Directions.LEFT,
                "ending_side": Directions.UP
            }
        }

    def move(self, *, movement_instruction: MovementInstruction | None = None):
        movement_instruction = movement_instruction or self.car_data_transmitter.get_movement_instruction()
        self.apply_movement_instruction(movement_instruction)
        super().move()
        return movement_instruction

    def apply_movement_instruction(self, movement_instruction: MovementInstruction):
        self._apply_speed_modification(movement_instruction['speed_modification'])
        self.turn(movement_instruction['turn_direction'])

    def _apply_speed_modification(self, modification: SpeedModifications):
        if modification == SpeedModifications.SPEED_UP:
            direction = Directions.FRONT if self.velocity >= 0 else Directions.BACK
            self.speed_up(direction)
        elif modification == SpeedModifications.NO_CHANGE:
            pass
        elif modification == SpeedModifications.BRAKE:
            self.brake()

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
            "manoeuvres": self.manoeuvres_description
        }