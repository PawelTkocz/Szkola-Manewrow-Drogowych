from enum import Enum
from typing import TypeAlias, TypedDict

from geometry import Point
from smart_city.schemas import LiveCarData

TrackPath: TypeAlias = list[tuple[float, float]]


class TurnSignal(Enum):
    RIGHT_SIGNAL = "right_signal"
    NO_SIGNAL = "no_signal"
    LEFT_SIGNAL = "left_signal"


class TrackPointData(TypedDict):
    point: Point
    max_safe_velocity: float
    turn_signal: TurnSignal


class EnteringZoneStatus(TypedDict):
    time_to_enter_zone: int
    live_car_data: LiveCarData
