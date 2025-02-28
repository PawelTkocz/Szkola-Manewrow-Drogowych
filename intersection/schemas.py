from typing import TypedDict

from car.car import LiveCarData
from geometry import Directions, Rectangle


class CarOnIntersection(TypedDict):
    live_car_data: LiveCarData
    starting_side: Directions
    ending_side: Directions


class IntersectionParts(TypedDict):
    intersection_area: Rectangle
    incoming_lines: dict[Directions, Rectangle]
    outcoming_lines: dict[Directions, Rectangle]
