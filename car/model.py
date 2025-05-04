from typing import TypedDict

from car.schemas import CarPartPosition


class ChassisSpecification(TypedDict):
    width: float
    length: float


class SteeringSystemSpecification(TypedDict):
    wheels_turn_speed: float
    wheels_max_angle: float


class WheelsSpecification(TypedDict):
    length: float
    width: float


class MotionSpecification(TypedDict):
    max_velocity: float
    acceleration: float
    brake_force: float
    rolling_resistance: float


class LightsSpecification(TypedDict):
    left: CarPartPosition
    right: CarPartPosition
    turn_signals_tick_interval: int


class BodySpecification(TypedDict):
    shell: CarPartPosition
    left_side_mirror: CarPartPosition
    right_side_mirror: CarPartPosition
    front_window: CarPartPosition
    left_window: CarPartPosition
    right_window: CarPartPosition
    rear_window: CarPartPosition


class CarModelSpecification(TypedDict):
    name: str
    chassis: ChassisSpecification
    steering_system: SteeringSystemSpecification
    wheels: WheelsSpecification
    lights: LightsSpecification
    motion: MotionSpecification
    body: BodySpecification
