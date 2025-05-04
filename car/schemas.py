from enum import Enum
from typing import TypeAlias, TypedDict


class CarPointPosition(TypedDict):
    """
    Representation of a point on a car.

    The (0, 0) point is the point in the middle of front bumper
    (the car is directed UP, paralelly to the Y axis).
    """

    x: float
    y: float


CarPartPosition: TypeAlias = list[CarPointPosition]


class CarBodyColors(TypedDict):
    shell: str
    windows: str
    side_mirrors: str


class ChassisColors(TypedDict):
    chassis: str
    wheels: str


class LightsColors(TypedDict):
    default: str
    turn_signal: str


class CarColors(TypedDict):
    body: CarBodyColors
    chassis: ChassisColors
    lights: LightsColors


class AccelerationDirection(Enum):
    FORWARD = "FORWARD"
    REVERSE = "REVERSE"
