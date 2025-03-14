from enum import Enum
from typing import TypedDict

from car.autonomous_car import LiveCarData
from geometry import Directions


class SpeedModifications(Enum):
    SPEED_UP = 1
    NO_CHANGE = 2
    BRAKE = 3


class MovementInstruction(TypedDict):
    speed_modification: SpeedModifications
    turn_direction: Directions  # create separate enum


class EnteringZoneStatus(TypedDict):
    time_to_enter_zone: int
    live_car_data: LiveCarData
