from typing import TypeAlias, TypedDict

from car.turn_signals import TurnSignalType
from geometry.direction import Direction
from geometry.vector import Point
from smart_city.schemas import LiveCarData

TrackPath: TypeAlias = list[tuple[float, float]]


class ManoeuvreTrackPoint(TypedDict):
    point: Point
    max_safe_velocity: float
    turn_signal: TurnSignalType


class EnteringZoneStatus(TypedDict):
    time_to_enter_zone: int
    live_car_data: LiveCarData


class ManoeuvreStartCarState(TypedDict):
    front_middle: Point
    direction: Direction
    wheels_angle: float
