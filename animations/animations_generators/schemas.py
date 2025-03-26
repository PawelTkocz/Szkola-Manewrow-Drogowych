from typing import TypedDict

from car.instruction_controlled_car import InstructionControlledCar, MovementInstruction
from geometry import Direction, Point
from smart_city.traffic_control_center import SmartTrafficCar


class PlaybackAnimationCarInfo(TypedDict):
    car: InstructionControlledCar
    movement_instructions: list[MovementInstruction]
    start_frame_number: int


class RuntimeAnimationCarInfo(TypedDict):
    car: SmartTrafficCar
    movement_instructions: list[MovementInstruction]
    start_frame_number: int


class CarStartingPosition(TypedDict):
    front_middle: Point
    direction: Direction
