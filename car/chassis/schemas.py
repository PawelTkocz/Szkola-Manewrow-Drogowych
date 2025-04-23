from typing import TypedDict

from car.schemas import CarPartPosition, CarPointPosition


class WheelPosition(TypedDict):
    middle: CarPointPosition
    corners: CarPartPosition


class WheelsPositions(TypedDict):
    left: WheelPosition
    right: WheelPosition
