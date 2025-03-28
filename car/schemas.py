from enum import Enum
from typing import TypeAlias, TypedDict


class GearboxState(Enum):
    REVERSE = "REVERSE"
    NEUTRAL = "NEUTRAL"
    DRIVE = "DRIVE"


class CarPointPosition(TypedDict):
    """
    Representation of a point on a car.

    The (0, 0) point is the point in the middle of front bumper
    (the car is directed UP, horizontally to the Y axis).
    """

    x: float
    y: float


# Position of a car part can be defined as list of points creating polygon
CarPartPosition: TypeAlias = list[CarPointPosition]
