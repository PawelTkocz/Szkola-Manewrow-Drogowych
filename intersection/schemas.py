from typing import TypedDict

from car.car_state import CarState
from geometry import Directions, Rectangle


class CarOnIntersection(TypedDict):
    car_state: CarState
    starting_side: Directions
    ending_side: Directions


class IntersectionParts(TypedDict):
    intersection_area: Rectangle
    incoming_lines: dict[Directions, Rectangle]
    outcoming_lines: dict[Directions, Rectangle]
