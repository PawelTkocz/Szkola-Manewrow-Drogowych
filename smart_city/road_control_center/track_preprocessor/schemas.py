from typing import TypedDict
from geometry import Direction, Point


class ManoeuvreStartCarState(TypedDict):
    front_middle: Point
    direction: Direction
    wheels_direction: Direction
