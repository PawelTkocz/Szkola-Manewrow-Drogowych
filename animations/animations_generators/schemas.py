from typing import TypedDict

from car.instruction_controlled_car import (
    CarControlInstructions,
    InstructionControlledCar,
)
from geometry import Direction, Point
from smart_city.smart_city_car import SmartCityCar


class PlaybackAnimationCarInfo(TypedDict):
    car: InstructionControlledCar
    movement_instructions: list[CarControlInstructions]
    start_frame_number: int


class RuntimeAnimationCarInfo(TypedDict):
    car: SmartCityCar
    movement_instructions: list[CarControlInstructions]
    start_frame_number: int


class CarStartingPosition(TypedDict):
    front_middle: Point
    direction: Direction
